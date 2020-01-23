#!/usr/bin/env bash
echo "Running HTTPS Transport Module."

dockerize -wait tcp://$QUEUE_HOST:$QUEUE_PORT -timeout 30s

# Start the first process
echo "Starting flask app"
python3 -u ./HTTPS/main.py
