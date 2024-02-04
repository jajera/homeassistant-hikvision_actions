FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

RUN apt-get update
RUN apt-get install -y --no-install-recommends \
        libudev-dev \
        libavformat-dev \
        libavcodec-dev \
        libavdevice-dev \
        libavutil-dev \
        libswscale-dev \
        libswresample-dev \
        libavfilter-dev \
        libpcap-dev \
        libturbojpeg0 \
        libyaml-dev \
        libxml2 \
        git \
        cmake \
        pip install --upgrade pip

WORKDIR /workspaces

# Install Python dependencies from requirements
COPY requirements_dev.txt ./
RUN pip3 install -r requirements_dev.txt
COPY requirements_test.txt ./
RUN pip3 install -r requirements_test.txt
RUN rm -rf requirements_dev.txt requirements_test.txt

# Set the default shell to bash instead of sh
ENV SHELL /bin/bash
