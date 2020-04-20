#!/bin/bash

while ! timeout 1 bash -c "echo > /dev/tcp/kafka/9093" > /dev/null 2>&1; do
  sleep 1
done
sleep 1

cd /worker || exit
FLASK_APP=water FLASK_ENV=development flask start_server_consumer
