#!/bin/bash

DATA_DIR=./data
HOST_NAME=localhost
HOST_PORT=9200
USER_NAME=elastic
PW=elastic

# NODE_TLS_REJECT_UNAUTHORIZED=0 elasticdump --input="${DATA_DIR}/linux-91-sysflow-bh22-20220727.mapping.json" --output="https://${USER_NAME}:${PW}@${HOST_NAME}:${HOST_PORT}/linux-91-sysflow-bh22-20220727" --type=mapping
# NODE_TLS_REJECT_UNAUTHORIZED=0 elasticdump --input="${DATA_DIR}/linux-91-sysflow-bh22-20220727.json" --output="https://${USER_NAME}:${PW}@${HOST_NAME}:${HOST_PORT}/linux-91-sysflow-bh22-20220727" --limit 25000 --type=data 

# Attack Data
NODE_TLS_REJECT_UNAUTHORIZED=0 elasticdump --input="${DATA_DIR}/winlogbeat-8.12.0.mapping.json" --output="https://${USER_NAME}:${PW}@${HOST_NAME}:${HOST_PORT}/winlogbeat-8.12.0" --type=mapping
NODE_TLS_REJECT_UNAUTHORIZED=0 elasticdump --input="${DATA_DIR}/winlogbeat-8.12.0.json" --output="https://${USER_NAME}:${PW}@${HOST_NAME}:${HOST_PORT}/winlogbeat-8.12.0" --limit 25000 --type=data 
NODE_TLS_REJECT_UNAUTHORIZED=0 elasticdump --input="${DATA_DIR}/filebeat-8.12.2.mapping.json" --output="https://${USER_NAME}:${PW}@${HOST_NAME}:${HOST_PORT}/filebeat-8.12.2" --type=mapping
NODE_TLS_REJECT_UNAUTHORIZED=0 elasticdump --input="${DATA_DIR}/filebeat-8.12.2.json" --output="https://${USER_NAME}:${PW}@${HOST_NAME}:${HOST_PORT}/filebeat-8.12.2" --limit 25000 --type=data 