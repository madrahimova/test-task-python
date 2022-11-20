#!/usr/bin/env sh

docker network create test
cd src/server && chmod +x run.sh && ./run.sh && cd ../client && chmod +x run.sh && ./run.sh