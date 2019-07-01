FROM oif/base:alpine-python3_utils

MAINTAINER Screaming_Bunny

LABEL name="COAP Transport Module" \
vendor="OpenC2" \
license="BSD" \
version="2.0" \
description="This is the Transport Module container"

ADD requirements.txt /tmp/requirements.txt
ADD COAP/ /opt/transport/COAP
ADD docker_dev_start.sh /opt/transport/COAP/dev_start.sh

RUN pip3 install -r /tmp/requirements.txt && \
    dos2unix /opt/transport/COAP/dev_start.sh && \
    chmod +x /opt/transport/COAP/dev_start.sh 

# Set working directory
WORKDIR /opt/transport/COAP

# Run command when container launches
CMD ["./dev_start.sh"]

