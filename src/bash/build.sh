#!/bin/bash

TAG='fem'
UPDATE_REPO='false'

function parse_args() {
  local OPTIND
  while getopts 'T:u' opt; do
    case "${opt}" in
      T)
        TAG="${OPTARG}"
        ;;
      u)
        UPDATE_REPO='true'
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

  if [[ "x${UPDATE_REPO}" == 'xtrue' ]]; then
      rm -rf ./diploma
      git clone https://github.com/kvendingoldo/diploma
  fi

  docker rmi -f kvendingoldo/diploma:${TAG}
  docker build -t kvendingoldo/diploma:${TAG} .
}

main "${@}"



