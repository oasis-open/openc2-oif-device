#!/bin/bash

echo "Run elastic container"

docker run \
      --name elasticsearch \
      --net elastic \
      -p 9200:9200 \
      -e discovery.type=single-node \
      -e ES_JAVA_OPTS="-Xms1g -Xmx1g"\
      -e ELASTIC_PASSWORD=elastic \
      -d \
      -it \
      docker.elastic.co/elasticsearch/elasticsearch:8.2.2
