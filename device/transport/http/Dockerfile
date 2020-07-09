# Image environment
FROM g2inc/oif-python
RUN apk upgrade --update && apk add --no-cache dos2unix && rm /var/cache/apk/*

MAINTAINER Screaming_Bunny

LABEL name="HTTP Transport Module" \
vendor="OpenC2" \
license="BSD" \
version="2.0" \
description="This is the HTTP Transport Module container"

ADD requirements.txt /tmp/requirements.txt
ADD docker_dev_start.sh /opt/transport/dev_start.sh

# Copy directories
ADD HTTP /opt/transport/HTTP

# Set working directory
WORKDIR /opt/transport

# Requirements install
RUN apk update && \
  apk add --no-cache \
  bash \
  openssl && \
  pip3 install -r /tmp/requirements.txt && \
  rm -r /root/.cache && \
  chmod +x /opt/transport/dev_start.sh && \
  dos2unix /opt/transport/dev_start.sh && \
#
# Cleanup
apk del tar && \
rm /var/cache/apk/* && \
rm -rf *.tar.gz* /usr/src /root/.gnupg /tmp/*
# Run command when container launches
CMD ["./dev_start.sh"]

