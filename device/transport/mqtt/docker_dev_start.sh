#!/usr/bin/env bash
dockerize -wait tcp://$QUEUE_HOST:$QUEUE_PORT -timeout 30s

echo "Running MQTT Transport Module."
python3 mqtt_transport.py