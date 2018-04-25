#!/bin/bash

CONTAINER_NAME='kvendingoldo-diploma-fem'
IMAGE_NAME='kvendingoldo/diploma:fem'

function parse_args() {
  local OPTIND
  while getopts 'I:C:' opt; do
    case "${opt}" in
      I)
        IMAGE_NAME="${OPTARG}"
        ;;
      C)
        CONTAINER_NAME="${OPTARG}"
        ;;
      \?)
        echo "[ERROR]: Invalid option: -${opt}"
        exit 1
        ;;
    esac
  done
  shift "$((OPTIND-1))"
}

function main() {
  parse_args "${@}"

  echo "[INFO] Start time: $(date +%F-%H%M)"
  docker rm -f ${CONTAINER_NAME}
  docker run -d \
  	--cpus=2.000 \
  	--log-driver json-file \
  	--name=${CONTAINER_NAME} \
  	-v /home/asharov/data:/data \
  	${IMAGE_NAME} \
  	python3 -u main.py

  echo "[INFO] End time: $(date +%F-%H%M)"
  echo "[INFO] ${0} has been successfully completed"
}

main "${@}"
