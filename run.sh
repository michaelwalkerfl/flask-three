#!/bin/bash
set -euo pipefail

if [ ! -f config.env ]; then
    cp config.env.example config.env
    echo "Created config.env from config.env.example. Review it, then re-run."
    exit 1
fi

# config.env supplies the variables used for interpolation in docker-compose.yml
docker compose --env-file config.env up --build
