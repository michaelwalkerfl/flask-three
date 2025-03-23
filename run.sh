#!/bin/bash

# load environment variables from config.env
set -a
source ./config.env
set +a

# run docker-compose
docker-compose up --build 