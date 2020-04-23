FROM g2inc/oif-python:latest

MAINTAINER Screaming_Bunny

LABEL name="Actuator ACDCI_UC9" \
vendor="OpenC2" \
license="BSD" \
version="v0.0.1" \
description="This is the ACDCI_UC9 Actuator container"

ADD requirements.txt /tmp/requirements.txt
ADD act_server /opt/actuator/act_server

# Package installation
# Packages - https://pkgs.alpinelinux.org/packages
#
# Requirements install
RUN pip3 install -r /tmp/requirements.txt && \
#
# Cleanup
rm -rf /var/cache/apk/* *.tar.gz* /usr/src /root/.gnupg /tmp/*