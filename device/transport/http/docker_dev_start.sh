#!/usr/bin/env bash
echo "Running HTTP Transport Module."

dockerize -wait tcp://$QUEUE_HOST:$QUEUE_PORT -timeout 30s

# Start the first process
echo "Starting flask app"
python3 -u ./HTTP/main.py
