FROM oif/base

MAINTAINER $MAINTAINER

LABEL name="Actuator ISR" \
vendor="OpenC2" \
license="BSD" \
version="$VERSION" \
description="This is the ISR Actuator container"

ENV PYTHONUNBUFFERED=1

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

# Orchestrator Core Working Directory
WORKDIR /opt/actuator/

# Startup Command
CMD ["./start.sh"]
