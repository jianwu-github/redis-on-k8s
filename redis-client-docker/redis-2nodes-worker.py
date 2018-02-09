import argparse
import pprint

import redis

import cv2

_DEFAULT_REDIS_SERVER_NAME = "localhost"  # "105.144.47.40"
_DEFAULT_REDIS_SERVER_PORT = 6379         # 32379

_DEFAULT_REDIS_DB = 0

_DEFAULT_TASK_ROOT_KEY = "tasks-for-two-workers"

_DEFAULT_INPUT_IMAGES_DIR = "input-images"
_DEFAULT_PROC_IMAGES_DIR = "proc-images"


arg_parser = argparse.ArgumentParser("env_handler")
arg_parser.add_argument("-workerid", type=str)
arg_parser.add_argument("-rsvrname", default=_DEFAULT_REDIS_SERVER_NAME)
arg_parser.add_argument("-rsvrport", type=int, default=_DEFAULT_REDIS_SERVER_PORT)
arg_parser.add_argument("-rdbid", type=int, default=_DEFAULT_REDIS_DB)


def process_image(image_file):
    input_image_file = _DEFAULT_INPUT_IMAGES_DIR + "/" + image_file
    output_image_file = _DEFAULT_PROC_IMAGES_DIR + "/proc-" +image_file

    input_image =cv2.imread(input_image_file)
    output_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(output_image_file, output_image)


def main(args):
    redis_db = redis.StrictRedis(host=args.rsvrname,
                                 port=args.rsvrport,
                                 db=args.rdbid)

    workers_tasks = redis_db.hgetall(_DEFAULT_TASK_ROOT_KEY)
    # pprint.pprint(workers_tasks)

    worker_id = args.workerid
    worker_task_id = workers_tasks[worker_id]
    file_list = redis_db.lrange(worker_task_id, 0, -1)

    print("workerid is {}, image file list is:".format(worker_id))
    pprint.pprint(file_list)

    for image_file in file_list:
        print("processing image file {} ...".format(image_file))
        process_image(image_file)


if __name__ == "__main__":
    args = arg_parser.parse_args()
    main(args)
