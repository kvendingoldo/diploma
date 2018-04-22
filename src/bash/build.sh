#!/bin/bash

docker rmi -f kvendingoldo/diploma:fem
docker rm -f kvendingoldo-diploma
docker build -t kvendingoldo/diploma:fem .
