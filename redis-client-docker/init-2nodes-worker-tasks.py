import sys
import os
import argparse
import pprint

import redis

_DEFAULT_REDIS_SERVER_NAME = "localhost" # ""105.144.47.40"
_DEFAULT_REDIS_SERVER_PORT = 6379 # 32379

_DEFAULT_REDIS_DB = 0

_DEFAULT_WORKER_ID = 0

arg_parser = argparse.ArgumentParser("init_worker-tasks")
arg_parser.add_argument("-rsvrname", default=_DEFAULT_REDIS_SERVER_NAME)
arg_parser.add_argument("-rsvrport", type=int, default=_DEFAULT_REDIS_SERVER_PORT)
arg_parser.add_argument("-rdbid", type=int, default=_DEFAULT_REDIS_DB)


def main(args):
    redis_db = redis.StrictRedis(host=args.rsvrname,
                                 port=args.rsvrport,
                                 db=args.rdbid)

    # create task for worker1
    worker1_file_list = "worker1-file-list"
    redis_db.lpush(worker1_file_list, "cat.1000.jpg")
    redis_db.lpush(worker1_file_list, "cat.1001.jpg")
    redis_db.lpush(worker1_file_list, "cat.1002.jpg")
    redis_db.lpush(worker1_file_list, "cat.1003.jpg")
    redis_db.lpush(worker1_file_list, "cat.1004.jpg")

    # create task for worker2
    worker2_file_list = "worker2-file-list"
    redis_db.lpush(worker2_file_list, "cat.1005.jpg")
    redis_db.lpush(worker2_file_list, "cat.1006.jpg")
    redis_db.lpush(worker2_file_list, "cat.1007.jpg")
    redis_db.lpush(worker2_file_list, "cat.1008.jpg")
    redis_db.lpush(worker2_file_list, "cat.1009.jpg")

    # create task schedule for 2 workers on 2 nodes
    redis_db.hmset("tasks-for-two-workers", {"worker1-task": "worker1-file-list", "worker2-task": "worker2-file-list"})

    print("Created tasks for 2 workers on 2 nodes")

if __name__ == "__main__":
    args = arg_parser.parse_args()
    main(args)
