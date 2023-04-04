FROM ccoe-gitlab-registry.hii-tsd.com/screamingbunny/docker/plus:alpine-python3

LABEL name="Logger Server" \
vendor="OpenC2" \
license="BSD" \
version="2.0" \
description="This is the Logger Server container"

ADD requirements.txt /tmp/requirements.txt
ADD syslog.py /opt/syslog/
COPY docker-entrypoint.sh /

# Package installation
# Packages - https://pkgs.alpinelinux.org/packages
#
# Requirements install
RUN apk add --no-cache --virtual .build-deps gcc python3-dev libc-dev && \
pip3 install -r /tmp/requirements.txt && \
# Entrypint config
chmod +x /docker-entrypoint.sh && \
# Cleanup
apk del .build-deps && \
rm -rf /var/cache/apk/* *.tar.gz* /usr/src /root/.gnupg /tmp/*

# Ports
EXPOSE 514/tcp

# Orchestrator Core Working Directory
WORKDIR /opt/syslog/

# Persistant volume
VOLUME '/var/log/syslog'

# Startup Command
ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["python3", "-u", "syslog.py"]
