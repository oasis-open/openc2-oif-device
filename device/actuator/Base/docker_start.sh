#!/usr/bin/env bash

echo "Running Base Actuator"

dockerize -wait tcp://$QUEUE_HOST:$QUEUE_PORT -wait tcp://$ETCD_HOST:$ETCD_PORT -timeout 30s

exec python3 -u act_server/start_actuator.py