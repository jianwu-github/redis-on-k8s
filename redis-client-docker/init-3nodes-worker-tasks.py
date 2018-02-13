import sys
import os
import argparse
import pprint

import redis

_DEFAULT_REDIS_SERVER_NAME = "localhost" # ""105.144.47.40"
_DEFAULT_REDIS_SERVER_PORT = 6379 # 32379

_DEFAULT_REDIS_DB = 0

_DEFAULT_WORKER_ID = 0

_THREE_WORKS_TASK_PREFIX = "three-works-tasks"

arg_parser = argparse.ArgumentParser("init_worker-tasks")
arg_parser.add_argument("-rsvrname", default=_DEFAULT_REDIS_SERVER_NAME)
arg_parser.add_argument("-rsvrport", type=int, default=_DEFAULT_REDIS_SERVER_PORT)
arg_parser.add_argument("-rdbid", type=int, default=_DEFAULT_REDIS_DB)


def main(args):
    redis_db = redis.StrictRedis(host=args.rsvrname,
                                 port=args.rsvrport,
                                 db=args.rdbid)

    # create task for worker1
    worker1_file_list = _THREE_WORKS_TASK_PREFIX + ":" + "worker1-task"
    redis_db.lpush(worker1_file_list, "cat.1010.jpg")
    redis_db.lpush(worker1_file_list, "cat.1011.jpg")
    redis_db.lpush(worker1_file_list, "cat.1012.jpg")
    redis_db.lpush(worker1_file_list, "cat.1013.jpg")
    redis_db.lpush(worker1_file_list, "cat.1014.jpg")

    # create task for worker2
    worker2_file_list = _THREE_WORKS_TASK_PREFIX + ":" + "worker2-task"
    redis_db.lpush(worker2_file_list, "cat.1015.jpg")
    redis_db.lpush(worker2_file_list, "cat.1016.jpg")
    redis_db.lpush(worker2_file_list, "cat.1017.jpg")
    redis_db.lpush(worker2_file_list, "cat.1018.jpg")
    redis_db.lpush(worker2_file_list, "cat.1019.jpg")

    # create task for worker3
    worker3_file_list = _THREE_WORKS_TASK_PREFIX + ":" + "worker3-task"
    redis_db.lpush(worker3_file_list, "cat.1020.jpg")
    redis_db.lpush(worker3_file_list, "cat.1021.jpg")
    redis_db.lpush(worker3_file_list, "cat.1022.jpg")
    redis_db.lpush(worker3_file_list, "cat.1023.jpg")
    redis_db.lpush(worker3_file_list, "cat.1024.jpg")

    print("Created tasks for 3 workers on 3 nodes")

if __name__ == "__main__":
    args = arg_parser.parse_args()
    main(args)
