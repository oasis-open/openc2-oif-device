# Package Installation
# Packages - https://pkgs.alpinelinux.org/packages
apk upgrade --update
apk add --no-cache --virtual .build-deps \
  g++ \
  gcc \
  musl-dev \
  yaml-dev \
  python3-dev

# SB_Utils install
cd /tmp/modules/twisted
python3 setup.py install
cd

# Cleanup
apk del .build-deps
rm -rf /var/cache/apk/* *.tar.gz* /usr/src /root/.gnupg /tmp/*

# Check versions
python3 --version
pip3 --version