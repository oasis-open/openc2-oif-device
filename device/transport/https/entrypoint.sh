#!/usr/bin/env bash
set -e

if [[ ! -f /opt/transport/HTTPS/certs/server.csr ]]; then
  # Create certs for flask app, not needed if using own certs
  openssl genrsa -des3 -passout pass:develop -out /opt/transport/HTTPS/certs/server.pass.key 2048
  openssl rsa -passin pass:develop -in /opt/transport/HTTPS/certs/server.pass.key -out /opt/transport/HTTPS/certs/server.key
  rm /opt/transport/HTTPS/certs/server.pass.key
  openssl req -new -key /opt/transport/HTTPS/certs/server.key -out /opt/transport/HTTPS/certs/server.csr \
    -subj "/C=US/O=flask/OU=Screaming Bunny"
  openssl x509 -req -days 365 -in /opt/transport/HTTPS/certs/server.csr -signkey /opt/transport/HTTPS/certs/server.key \
    -out /opt/transport/HTTPS/certs/server.crt
fi

exec "$@"