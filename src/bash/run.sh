#!/bin/bash

CONTAINER_NAME='kvendingoldo-diploma'
IMAGE='kvendingoldo/diploma:fem'
DATA_DIR='/home/asharov/data'
CPUS='6.000'

function parse_args() {
  local OPTIND
  while getopts 'I:N:C:D:' opt; do
    case "${opt}" in
      I)
        IMAGE="${OPTARG}"
        ;;
      N)
        CONTAINER_NAME="${OPTARG}"
        ;;
      C)
        CPUS="${OPTARG}"
        ;;
      D)
        DATA_DIR="${OPTARG}"
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
  	--cpus=${CPUS} \
  	--log-driver json-file \
  	--name="${CONTAINER_NAME}" \
  	-v ${DATA_DIR}:/data \
  	"${IMAGE}" \
  	python3 -u main.py

  echo "[INFO] End time: $(date +%F-%H%M)"
  echo "[INFO] ${0} has been successfully completed"
}

main "${@}"
