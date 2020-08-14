#!/usr/bin/env bash

echo "Running COAP Transport Module."
dockerize -wait tcp://$QUEUE_HOST:$QUEUE_PORT -timeout 30s

echo "Starting CoAP Server"
python3 -u ./COAP/coap_server.py &
status=$?
if [[ $status -ne 0 ]]; then
  echo "Failed to start CoAP Server: $status"
  exit $status
fi

echo "Starting CoAP Client"
python3 -u ./COAP/coap_client.py
status=$?
if [[ $status -ne 0 ]]; then
  echo "Failed to start CoAP Client: $status"
  exit $status
fi