from redis import StrictRedis
from rq import get_current_job

def backend_job1():
    print("running backend job1 ...")
