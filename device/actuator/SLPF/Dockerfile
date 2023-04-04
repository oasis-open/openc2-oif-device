FROM screambunn/alpine-python3_actuator

LABEL name="Actuator SLPF" \
vendor="OpenC2" \
license="BSD" \
version="v0.0.1" \
description="This is the SLPF Actuator container"

ADD requirements.txt /tmp/requirements.txt
ADD docker_start.sh /opt/actuator/start.sh
ADD act_server /opt/actuator/act_server

# Package installation
# Packages - https://pkgs.alpinelinux.org/packages
#
# Requirements install
RUN pip3 install -r /tmp/requirements.txt && \ && \
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
