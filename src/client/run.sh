#!/usr/bin/env sh

image=test-task-client
docker build . -t $image && docker run --name test-task-client --net test -p 8080:8080 -d $image