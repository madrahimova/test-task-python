#!/usr/bin/env sh

docker network create test
cd src/server && run.sh && cd ../client && run.sh