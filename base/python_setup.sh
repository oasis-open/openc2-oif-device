# Package Installation
# Packages - https://pkgs.alpinelinux.org/packages
apk upgrade --update
apk add --no-cache python3 wget
apk add --no-cache --virtual .build-deps \
  g++ \
  gcc \
  musl-dev \
  yaml-dev \
  python3-dev

# Python PIP Install
wget -q https://bootstrap.pypa.io/get-pip.py | python3
pip3 install --upgrade pip
#
# SB_Utils install
cd /tmp/modules/root
python3 setup.py install
cd

# Cleanup
apk del .build-deps
rm -rf /var/cache/apk/* *.tar.gz* /usr/src /root/.gnupg /tmp/*

# Check versions
python3 --version
pip3 --version
