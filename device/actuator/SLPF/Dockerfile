FROM g2inc/oif-python:latest

MAINTAINER Screaming_Bunny

LABEL name="Actuator SLPF" \
vendor="OpenC2" \
license="BSD" \
version="v0.0.1" \
description="This is the SLPF Actuator container"

ENV PYTHONUNBUFFERED=1

ADD requirements.txt /tmp/requirements.txt
ADD act_server /opt/actuator/act_server
ADD docker_start.sh /opt/actuator/start.sh

# Package installation
# Packages - https://pkgs.alpinelinux.org/packages
#
# Requirements install
RUN apk add --no-cache --virtual .build-deps gcc musl-dev && \
pip3 install -r /tmp/requirements.txt && \
#
# Mod Startup Scripts
chmod +x /opt/actuator/start.sh && \
dos2unix /opt/actuator/start.sh && \
#
# Cleanup
apk del .build-deps && \
rm -rf /var/cache/apk/* *.tar.gz* /usr/src /root/.gnupg /tmp/*

# Actuator Working Directory
WORKDIR /opt/actuator/

# Startup Command
CMD ["./start.sh"]
