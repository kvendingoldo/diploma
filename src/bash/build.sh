#!/bin/bash

#rm -rf diploma
#git clone https://github.com/kvendingoldo/diploma

docker rmi -f kvendingoldo/diploma:fem
docker rm -f kvendingoldo-diploma
docker build -t kvendingoldo/diploma:fem .
