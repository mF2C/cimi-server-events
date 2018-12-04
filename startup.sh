#!/bin/sh -e

(cd /data && redis-server &)

PORT=$(cat ./config/config.json | jq .port)

export PYTHONPATH=$(pwd)/jobs
gunicorn sse:app --worker-class gevent --bind 0.0.0.0:$PORT
