#!/bin/bash

echo "Removing elasticsearch containers"

docker stop /elasticsearch
docker rm /elasticsearch

docker stop /kibana
docker rm /kibana

docker network rm elastic