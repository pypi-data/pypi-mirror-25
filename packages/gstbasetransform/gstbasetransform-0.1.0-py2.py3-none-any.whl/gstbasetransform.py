# -*- coding: utf-8 -*-
# Copyright (C) 2016 Dustin Spicuzza <dustin@virtualroadside.com>
# Copyright (C) 2017 Muges

"""
:mod:`gstbasetransform` is a module that provides a patched
:class:`GstBase.BaseTransform` that makes the `do_transform_size` virtual
method usable in python.
"""
# pylint: disable=import-error,wrong-import-position,too-few-public-methods
__version__ = "0.1.0"

import ctypes
from six import with_metaclass
import gi
from gi.types import GObjectMeta
gi.require_version('GIRepository', '2.0')
gi.require_version('Gst', '1.0')
gi.require_version('GstBase', '1.0')

from gi.repository import GIRepository, GObject, Gst, GstBase

# Load the GObject library via GIRepository
REPOSITORY = GIRepository.Repository.get_default()
GOBJECT_DLL_NAME = REPOSITORY.get_shared_library('GObject').split(',')[0]
GOBJECT_DLL = ctypes.CDLL(GOBJECT_DLL_NAME)

# Load the functions that we need
# pylint: disable=invalid-name
g_value_set_object = GOBJECT_DLL.g_value_set_object
g_value_set_object.argtypes = (ctypes.c_void_p, ctypes.c_void_p)

g_value_set_static_boxed = GOBJECT_DLL.g_value_set_static_boxed
g_value_set_static_boxed.argtypes = (ctypes.c_void_p, ctypes.c_void_p)

# A function prototype that create functions with the same signature as the
# transform_size virtual method.
#
#  gboolean (*transform_size) (GstBaseTransform *trans,
#                              GstPadDirection direction,
#                              GstCaps *caps,
#                              gsize size,
#                              GstCaps *othercaps,
#                              gsize *othersize);
transform_size_functype = ctypes.CFUNCTYPE(
    ctypes.c_bool, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p,
    ctypes.c_long, ctypes.c_void_p, ctypes.POINTER(ctypes.c_long))
# pylint: enable=invalid-name


def vfunc_info_get_address(vfunc_info, gtype):
    """Returns the address of a virtual function.

    This function is similar to `GIRepository.vfunc_info_get_address`, except
    that it does not dereference the address before returning it.

    :param vfunc_info: a GIRepository.BaseInfo.
    :type vfunc_info: GIRepository.BaseInfo
    :param gtype: `GObject.GType` implementing this virtual function.
    :type gtype: GObject.GType
    :return: the address of the function as an integer.
    """
    container_info = vfunc_info.get_container()
    implementor_class = GObject.type_class_ref(gtype)
    if container_info.get_type() == GIRepository.InfoType.OBJECT:
        struct_info = GIRepository.object_info_get_class_struct(container_info)
        implementor_vtable = implementor_class
    else:
        struct_info = (
            GIRepository.interface_info_get_iface_struct(container_info)
        )

        interface_type = (
            GIRepository.registered_type_info_get_g_type(container_info)
        )
        implementor_vtable = (
            GObject.type_interface_peek(implementor_class, interface_type)
        )

    field_info = (
        GIRepository.struct_info_find_field(struct_info, vfunc_info.get_name())
    )

    if field_info is None:
        raise AttributeError("Could not find struct field for vfunc")

    offset = GIRepository.field_info_get_offset(field_info)
    return hash(implementor_vtable) + offset


class BaseTransformMeta(GObjectMeta):
    """Metaclass that modifies the :class:`BaseTransform` class to make the
    `do_transform_size` virtual method usable in python."""
    # pylint: disable=no-self-argument
    # We use cls instead of self, since this is a metaclass.

    def __init__(cls, name, bases, attrs):
        GObjectMeta.__init__(cls, name, bases, attrs)

        do_transform_size = attrs.get('do_transform_size')
        if do_transform_size is None:
            return

        # Get the transform_size vfunc
        for base in cls.__mro__:
            typeinfo = REPOSITORY.find_by_gtype(base.__gtype__)
            if typeinfo:
                vfunc = GIRepository.object_info_find_vfunc_using_interfaces(
                    typeinfo, 'transform_size')
                if vfunc:
                    break
        else:
            raise AttributeError("Could not find vfunc for transform_size")

        # Get the address of the vfunc so we can put our own callback in there
        address = vfunc_info_get_address(vfunc[0], cls.__gtype__)

        # Make a thunk function closure, store it so it doesn't go out of scope
        do_transform_size.wrapper = cls._wrap_do_transform_size()

        # Don't judge me... couldn't get a normal function pointer to work
        dbl_pointer = ctypes.POINTER(ctypes.c_void_p)
        addr = ctypes.cast(address, dbl_pointer)
        addr.contents.value = (
            ctypes.cast(do_transform_size.wrapper, ctypes.c_void_p).value
        )

    def _wrap_do_transform_size(cls):
        """Constructs a custom thunk function for each class.

        This is in a closure so that we can use the class to construct a
        GObject.Value for converting the widget object.
        """

        def _transform_size(raw_trans, direction, raw_caps, size,
                            raw_othercaps, raw_othersize):
            """Static function that gets inserted as the transform_size
            vfunction, instead of using the vfunction implementation provided
            by pygobject

            This function exists so that we can modify the size of the output
            buffer.
            """
            # pylint: disable=too-many-arguments

            # Grab the python wrapper for the widget instance
            value = GObject.Value(cls)
            g_value_set_object(hash(value), raw_trans)
            basetransform = value.get_object()

            # Convert the caps to a python object
            value = GObject.Value(Gst.Caps)
            g_value_set_static_boxed(hash(value), raw_caps)
            caps = value.get_boxed()

            value = GObject.Value(Gst.Caps)
            g_value_set_static_boxed(hash(value), raw_othercaps)
            othercaps = value.get_boxed()

            # Call the original virtual function with the converted arguments
            retval, othersize = basetransform.do_transform_size(
                direction, caps, size, othercaps)

            raw_othersize.contents.value = othersize

            return retval

        return transform_size_functype(_transform_size)


class BaseTransform(with_metaclass(BaseTransformMeta, GstBase.BaseTransform)):
    """A :class:`GstBase.BaseTransform` patched to make the `do_transform_size`
    virtual method usable in python."""
    # pylint: disable=invalid-metaclass,no-init
    pass
