# Image environment
FROM oif/base:alpine-python3_utils

MAINTAINER Screaming_Bunny

LABEL name="HTTPS Transport Module" \
vendor="OpenC2" \
license="BSD" \
version="2.0" \
description="This is the HTTPS Transport Module container"

ADD requirements.txt /tmp/requirements.txt
ADD docker_dev_start.sh /opt/transport/dev_start.sh

# Copy directories
ADD HTTPS/ /opt/transport/HTTPS

# Set working directory
WORKDIR /opt/transport

# Requirements install
RUN apk update
RUN apk add --no-cache \
    bash \
    openssl && \
    pip3 install -r /tmp/requirements.txt && \
    rm -r /root/.cache && \
    chmod +x /opt/transport/dev_start.sh && \
    chmod +w /opt/transport/HTTPS/certs && \
    dos2unix /opt/transport/dev_start.sh

# Create certs for flask app, not needed if using own certs
RUN openssl genrsa -des3 -passout pass:develop -out /opt/transport/HTTPS/certs/server.pass.key 2048 && \
    openssl rsa -passin pass:develop -in /opt/transport/HTTPS/certs/server.pass.key -out /opt/transport/HTTPS/certs/server.key && \
    rm /opt/transport/HTTPS/certs/server.pass.key && \
    openssl req -new -key /opt/transport/HTTPS/certs/server.key -out /opt/transport/HTTPS/certs/server.csr \
        -subj "/C=US/O=flask/OU=Screaming Bunny" && \
    openssl x509 -req -days 365 -in /opt/transport/HTTPS/certs/server.csr -signkey /opt/transport/HTTPS/certs/server.key -out /opt/transport/HTTPS/certs/server.crt

# Run command when container launches
CMD ["./dev_start.sh"]

