#!/bin/bash

IMAGE_TAG="${1}"

docker rmi -f kvendingoldo/diploma:${IMAGE_TAG}
docker build -t kvendingoldo/diploma:${IMAGE_TAG} .
