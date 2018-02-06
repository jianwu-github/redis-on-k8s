import sys
import os
import argparse
import pprint

import redis

from pywebhdfs.webhdfs import PyWebHdfsClient


_DEFAULT_REDIS_SERVER_NAME = "105.144.47.40"
_DEFAULT_REDIS_SERVER_PORT = 32379

_DEFAULT_REDIS_DB = 0

_DEFAULT_WORKER_ID = 0

arg_parser = argparse.ArgumentParser("env_handler")
arg_parser.add_argument("rsvrname", default=_DEFAULT_REDIS_SERVER_NAME)
arg_parser.add_argument("rsvrport", type=int, default=_DEFAULT_REDIS_SERVER_PORT)
arg_parser.add_argument("rdbid", type=int, default=_DEFAULT_REDIS_DB)


def _get_task_list(worker_id):
    return "worker" + str(worker_id) + "-task-list"


def main(args):
    redis_db = redis.StrictRedis(host=args.rsvrname,
                                 port=args.rsvrport,
                                 db=args.rdbid)

    task_list = _get_task_list(_DEFAULT_WORKER_ID)

    redis_db.lpush(task_list, "cat.1000.jpg")
    redis_db.lpush(task_list, "cat.1001.jpg")
    redis_db.lpush(task_list, "cat.1002.jpg")
    redis_db.lpush(task_list, "cat.1003.jpg")
    redis_db.lpush(task_list, "cat.1004.jpg")

    task_items = redis_db.lrange(task_list, 0, -1)

    pprint.pprint(task_items)


if __name__ == "__main__":
    args = arg_parser.parse_args()
    main(args)
