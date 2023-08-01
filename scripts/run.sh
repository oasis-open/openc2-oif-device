#!/bin/bash

# CURRENTLY NOT WORKING *************************

set -e
trap 'last_command=$current_command; current_command=$BASH_COMMAND' DEBUG
trap 'echo "\"${last_command}\" command filed with exit code $?."' EXIT

sudo ./scripts/cleanup.sh
sudo ./scripts/start-network.sh
sudo ./scripts/start-elastic.sh
sudo ./scripts/start-kibana.sh
# sudo ./scripts/generate-token.sh
# sudo ./scripts/copy-cert.sh

echo "Open Kibana"
python3 -m webbrowser http://localhost:5601?code=038409    