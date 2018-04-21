#!/bin/bash

echo "[INFO] Start time: $(date +%F-%H%M)"
docker rm -f kvendingoldo-diploma
time docker run -it --name=kvendingoldo-diploma -v /home/asharov/data:/data kvendingoldo/diploma:fem python3 main.py
echo "[INFO] End time: $(date +%F-%H%M)"
