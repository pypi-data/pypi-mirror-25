FROM fedora:25

ENV LANG C.utf8

RUN dnf -y install \
    gstreamer1-plugins-base \
    python-pip \
    python-setuptools \
    pygobject3 \
    python3-gobject \
    python-gstreamer1

COPY requirements.txt /
RUN pip3 install -r /requirements.txt
