FROM g2inc/oif-python_twisted
RUN apk upgrade --update && apk add --no-cache dos2unix && rm /var/cache/apk/*

MAINTAINER Screaming_Bunny

LABEL name="Actuator Base" \
vendor="OpenC2" \
license="BSD" \
version="v0.0.1" \
description="This is the Base Actuator container"

ADD requirements.txt /tmp/requirements.txt
ADD act_server /opt/actuator/act_server
ADD docker_start.sh /opt/actuator/start.sh

# Package installation
# Packages - https://pkgs.alpinelinux.org/packages
#
# Requirements install
RUN pip3 install -r /tmp/requirements.txt && \
#
# Mod Startup Scripts
chmod +x /opt/actuator/start.sh && \
dos2unix /opt/actuator/start.sh && \
#
# Cleanup
rm -rf /var/cache/apk/* *.tar.gz* /usr/src /root/.gnupg /tmp/*

# Actuator Working Directory
WORKDIR /opt/actuator/

# Startup Command
CMD ["./start.sh"]
