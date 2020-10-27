#!/usr/bin/env bash
dockerize -wait tcp://$QUEUE_HOST:$QUEUE_PORT -wait tcp://$ETCD_HOST:$ETCD_PORT -timeout 30s

echo "Running MQTT Transport Module."
python3 -u mqtt_transport.py