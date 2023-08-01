#!/bin/bash

echo "Generate login token"
sudo docker exec -it elasticsearch \
    /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token \
    -s kibana