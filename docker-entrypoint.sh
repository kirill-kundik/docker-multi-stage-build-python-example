#!/usr/bin/env bash

./wait-for-it.sh elasticsearch:9200 -- gunicorn --workers=4 --bind="0.0.0.0:8080" --worker-class="uvicorn.workers.UvicornWorker" "main:app"
