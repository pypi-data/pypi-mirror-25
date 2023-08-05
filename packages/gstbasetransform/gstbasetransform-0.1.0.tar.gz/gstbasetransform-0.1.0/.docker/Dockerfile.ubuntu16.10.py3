FROM ubuntu:yakkety

ENV LANG C.UTF-8

RUN apt-get update && apt-get install --no-install-recommends -y \
    gir1.2-glib-2.0 \
    gir1.2-gstreamer-1.0 \
    gir1.2-gst-plugins-base-1.0 \
    gstreamer1.0-plugins-base \
    python3-pip \
    python3-setuptools \
    python3-gi \
    python3-gst-1.0

COPY requirements.txt /
RUN pip3 install -r /requirements.txt
