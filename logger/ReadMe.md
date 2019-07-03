# OASIS TC Open: oif-logger

## About this Image
This image is Alpine 3.10 with a simple syslog server and GUI for use with [Elasticsearch](https://hub.docker.com/_/elasticsearch)

## How to use this image
Note: Pulling an images requires using a specific tag (server or gui), the latest tag is not supported.

Environment Variables (Server)

| Variable | Type | Description | Default|
| ----------- | ----------- | ----------- | ----------- |
| ES_HOST | String | Host/IP of the Elasticsearch node | es_logger
| ES_PORT | Integer | Port of the Elasticsearch Node | 9200
| LOG_PREFIX | String | Prefix for the index in the format of `log_{LOG_PREFIX}-{YYYY.mm.dd}`  | logger

Environment Variables (GUI)

| Variable | Type | Description | Default|
| ----------- | ----------- | ----------- | ----------- |
| ES_HOST | String | Host/IP of the Elasticsearch node | es_logger
| ES_PORT | Integer | Port of the Elasticsearch Node | 9200
