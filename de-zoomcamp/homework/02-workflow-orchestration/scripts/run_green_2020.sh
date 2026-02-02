#!/bin/bash

for month in $(seq -w 1 12); do
  curl -v \
    -u "admin@kestra.io:Admin1234" \
    -H 'Content-Type: multipart/form-data' \
    -F 'taxi=green' \
    -F 'year=2020' \
    -F "month=${month}" \
    'http://localhost:8080/api/v1/main/executions/zoomcamp/homework_02'

  sleep 30
done
