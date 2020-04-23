#!/usr/bin/env bash
# Creates Docker images for actuators

BASEDIR=$(dirname "$0")
IMAGE_NAME=$1

for DIR in $BASEDIR/*/; do
  if [ "$DIR" != "${BASEDIR}/Base/" ]; then
    TAG=$(python3 -c "import re; print(re.sub(r'(^\./|/$)', '', \"${DIR}\").lower())")
    if [[ -f "${DIR}Dockerfile" ]]; then
        echo -e "Building $IMAGE_NAME:$TAG\n"
        docker build --no-cache -f ${DIR}Dockerfile -t $IMAGE_NAME:$TAG $DIR
    else
        echo -e "No Dockerfile found for ${TAG}\n\n"
    fi
    echo -e "-----------------------------------------------------------------------\n\n"
  fi
done
