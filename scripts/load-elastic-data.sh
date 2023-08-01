#!/bin/bash

#DATA_DIR="${HOME}"/workspace/oif-kestrel/data
DATA_DIR=./data
HOST_NAME=localhost
HOST_PORT=9200
USER_NAME=elastic
PW=elastic

NODE_TLS_REJECT_UNAUTHORIZED=0 elasticdump --input="${DATA_DIR}/linux-91-sysflow-bh22-20220727.mapping.json" --output="https://${USER_NAME}:${PW}@${HOST_NAME}:${HOST_PORT}/linux-91-sysflow-bh22-20220727" --type=mapping
NODE_TLS_REJECT_UNAUTHORIZED=0 elasticdump --input="${DATA_DIR}/linux-91-sysflow-bh22-20220727.json" --output="https://${USER_NAME}:${PW}@${HOST_NAME}:${HOST_PORT}/linux-91-sysflow-bh22-20220727" --limit 25000 --type=data 