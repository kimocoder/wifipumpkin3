FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
    && apt-get -y install \
        hostapd \
	    nano \
	    iw \
        wireless-tools \
        ifupdown \
        python3.8 \
        python3-pip \
        python3.8-dev \
        iptables \
        net-tools \
        rfkill \
        libpcap-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
# copy all files to app folder
COPY . /usr/src/app
WORKDIR /usr/src/app
COPY config/hostapd/hostapd.conf /etc/hostapd/hostapd.conf
#RUN pip3 --version
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
RUN python3.8 -m pip install --upgrade pip
RUN python3.8 -m pip install pyqt5==5.14
RUN python3.8 -m pip install .
#CMD /usr/local/bin/wifipumpkin3 -m docker
WORKDIR /root/.config/wifipumpkin3
CMD /usr/local/bin/wifipumpkin3
