#!/usr/bin/env bash

python redis-3nodes-worker.py -workerid ${WORKER_ID} -rsvrname ${REDIS_SERVER_NAME} -rsvrport ${REDIS_SERVER_PORT}