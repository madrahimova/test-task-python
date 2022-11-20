set image=test-task-server
docker build . -t %image% && docker run --name test-task-server --net test -p 12345:12345 -d %image%