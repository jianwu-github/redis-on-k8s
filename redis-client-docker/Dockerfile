FROM ubuntu:16.04

MAINTAINER Jian Wu <hellojianwu@gmail.com>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
    ca-certificates \
    gcc \
    git \
    libpq-dev \
    make \
    python2.7 \
    python2.7-dev \
    python-pip \
    python-mock \
    python-nose \
    python-coverage \
    pylint \
    ssh \
	python-zmq \
    && apt-get autoremove \
    && apt-get clean

RUN pip install -U setuptools

RUN apt-get -y update &&\
	apt-get install -y build-essential \
	cmake \
	qt5-default \
	libvtk6-dev \
	zlib1g-dev \
	libjpeg-dev \
	libwebp-dev \
	libpng-dev \
	libtiff5-dev \
	libjasper-dev \
	libopenexr-dev \
	libgdal-dev \
	libdc1394-22-dev \
	libavcodec-dev \
	libavformat-dev \
	libswscale-dev \
	libtheora-dev  \
	libvorbis-dev \
	libxvidcore-dev \
	libx264-dev  \
	yasm  \
	libopencore-amrnb-dev  \
	libopencore-amrwb-dev  \
	libv4l-dev  \
	libxine2-dev \
	libtbb-dev  \
	libeigen3-dev \
	python-dev  \
	python-tk  \
	python-numpy  \
	python3-dev  \
	python3-tk  \
	python3-numpy  \
	unzip  \
	wget &&\
	apt-get autoremove &&\
        apt-get clean
	
RUN cd /tmp && \
	wget https://github.com/opencv/opencv/archive/3.2.0.zip && \
	unzip 3.2.0.zip && \
	rm 3.2.0.zip && \
	mv opencv-3.2.0 OpenCV && \
	cd OpenCV && \
	mkdir build && \
	cd build && \
	cmake -DWITH_QT=ON -DWITH_OPENGL=ON -DFORCE_VTK=ON -DWITH_TBB=ON -DWITH_GDAL=ON -DWITH_XINE=ON -DBUILD_EXAMPLES=ON .. && \
	make -j4  && \
	make install && \
	ldconfig

RUN rm -rf /tmp

RUN pip --no-cache-dir install \
    http://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-1.4.0-cp27-none-linux_x86_64.whl

RUN pip install redis

RUN pip install pywebhdfs

# Define default command.
CMD ["python"]
