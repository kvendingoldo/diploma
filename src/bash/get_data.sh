#!/bin/bash

TIMESTAMP=$(date +%F-%H%M)

tar -cvjf ${TIMESTAMP}.tar.bz2 /home/asharov/data
