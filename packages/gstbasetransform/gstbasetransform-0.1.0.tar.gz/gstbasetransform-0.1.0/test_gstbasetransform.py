# -*- coding: utf-8 -*-

"""
A simple test for the gstbasetransform module.
"""
# pylint: disable=import-error,unused-argument,no-self-use,no-init

import sys
import gi
gi.require_version('Gst', '1.0')

# pylint: disable=wrong-import-position
from gi.repository import GObject, Gst
from gstbasetransform import BaseTransform
# pylint: enable=wrong-import-position

Gst.init(sys.argv)


class FixedSize(BaseTransform):
    """A filter that ignores its input data, and pushes zero-filled buffers of
    fixed size to the output."""
    __gstmetadata__ = (
        'Dummy', 'Transform', 'Dummy filter', 'Muges'
    )

    __gsttemplates__ = (Gst.PadTemplate.new("src",
                                            Gst.PadDirection.SRC,
                                            Gst.PadPresence.ALWAYS,
                                            Gst.Caps.new_any()),
                        Gst.PadTemplate.new("sink",
                                            Gst.PadDirection.SINK,
                                            Gst.PadPresence.ALWAYS,
                                            Gst.Caps.new_any()))

    def do_transform(self, in_buffer, out_buffer):
        """Process the data from in_buffer, and write the result to out_buffer.

        :param in_buffer: a ``Gst.Buffer`` containing the input data.
        :param out_buffer: a ``Gst.Buffer`` where the output data will be
            written.
        """
        # There is a bug that increases the refcount of out_buffer, making it
        # non writable (https://bugzilla.gnome.org/show_bug.cgi?id=727702#c4).
        # Set the refcount to 1 to fix this.
        refcount = out_buffer.mini_object.refcount
        out_buffer.mini_object.refcount = 1

        # Check that do_transform_size works
        size = out_buffer.get_size()
        if size != 2048:
            print("unexpected buffer size")
            return Gst.FlowReturn.ERROR
        print("out_buffer size is {} as expected".format(size))

        # Fill buffer with zeros
        data = bytes(2048)
        out_buffer.fill(0, data)

        # Reset the refcount
        out_buffer.mini_object.refcount = refcount

        return Gst.FlowReturn.OK

    def do_transform_size(self, direction, caps, size, othercaps):
        """Given the size of a buffer in the given direction with the given
        caps, calculate the size in bytes of a buffer on the other pad with the
        given other caps."""
        # Set the size of the output buffer to 2048 bytes
        return True, 2048


def plugin_init(plugin):
    """Initialize the plugin."""
    plugin_type = GObject.type_register(FixedSize)
    Gst.Element.register(plugin, 'fixedsize', 0, plugin_type)
    return True


Gst.Plugin.register_static(
    Gst.VERSION_MAJOR, Gst.VERSION_MINOR, 'fixedsize',
    'Dummy filter', plugin_init, '1',
    'LGPL', 'fixedsize', 'fixedsize', '')


def main():
    """Run the test."""
    pipeline = Gst.parse_launch(
        'audiotestsrc num-buffers=20 ! audioconvert ! fixedsize ! fakesink'
    )

    bus = pipeline.get_bus()
    bus.add_signal_watch()

    loop = GObject.MainLoop()

    def on_error(bus, message):
        """Called when there was an error during the playback."""
        pipeline.set_state(Gst.State.NULL)
        sys.exit(message.parse_error())
    bus.connect('message::error', on_error)

    def on_eos(bus, message):
        """Called at the end of the playback."""
        pipeline.set_state(Gst.State.NULL)
        sys.exit(0)
    bus.connect('message::eos', on_eos)

    pipeline.set_state(Gst.State.PLAYING)
    loop.run()

    pipeline.set_state(Gst.State.NULL)


if __name__ == '__main__':
    main()
