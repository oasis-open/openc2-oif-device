# Package installation
# Packages - https://pkgs.alpinelinux.org/packages
apk upgrade --update
apk add --no-cache bash \
    shadow \
    tar \
    dos2unix \
    wget

# Dockerize Config
wget -q https://github.com/jwilder/dockerize/releases/download/${DOCKERIZE_VERSION}/dockerize-alpine-linux-amd64-${DOCKERIZE_VERSION}.tar.gz -O /tmp/dockerize.tar.gz
tar -C /usr/local/bin -xzvf /tmp/dockerize.tar.gz
#
# Cleanup
apk del tar wget
rm -rf /var/cache/apk/* *.tar.gz* /usr/src /root/.gnupg /tmp/*
