#!/bin/bash

echo "Copy ca cert"
docker cp elasticsearch:/usr/share/elasticsearch/config/certs/http_ca.crt .