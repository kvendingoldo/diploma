#!/bin/bash

TAG='fem'
BUILD_BASE='false'

function parse_args() {
  local OPTIND
  while getopts 'T:b' opt; do
    case "${opt}" in
      T)
        TAG="${OPTARG}"
        ;;
      b)
        BUILD_BASE='true'
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

  BUILD_DIR="/tmp/${TAG}"

  mkdir ${BUILD_DIR}

  cp -r ../../src/docker ${BUILD_DIR}
  cp -r ../../src/python ${BUILD_DIR}
  cp -r ../../resources ${BUILD_DIR}

  cd ${BUILD_DIR}

  if [[ "x${BUILD_BASE}" == 'xtrue' ]]; then
    cp docker/Dockerfile.base Dockerfile
    docker rmi -f kvendingoldo/diploma:base
    docker build -t kvendingoldo/diploma:base .
    rm -rf Dockerfile
  fi

  cp docker/Dockerfile.app Dockerfile
  docker rmi -f kvendingoldo/diploma:${TAG}
  docker build -t kvendingoldo/diploma:${TAG} .

  cd -
  rm -rf ${BUILD_DIR}
}

main "${@}"



