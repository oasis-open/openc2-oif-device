#!/usr/bin/env bash
echo "Running HTTPS Transport Module."

dockerize -wait tcp://$QUEUE_HOST:$QUEUE_PORT -timeout 30s

# Start the first process
echo "Starting flask app"
python3 -u ./HTTPS/main.py &
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start flask app: $status"
  exit $status
fi

# Start the second process
echo "Starting message sender"
python3 -u ./HTTPS/https_transport.py
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start message sender: $status"
  exit $status
fi
