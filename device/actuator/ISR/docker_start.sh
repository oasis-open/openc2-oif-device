#!/usr/bin/env bash

dockerize -wait tcp://$QUEUE_HOST:$QUEUE_PORT -timeout 30s

python3 -m act_server