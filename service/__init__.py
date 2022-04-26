import redis
import requests
import time


from service import (
    db,
    service_discover
)

from flask_apscheduler import APScheduler


URL = "https://lab.karpov.courses/hardml-api/module-5/get_secret_number"


def get_secret_number():
    while True:
        response = requests.get(URL)
        if response.status_code == 200:
            db.secret_number = response.json()['secret_number']
            break
        else:
            time.sleep(1)


def init_redis(host: str, port: int, password: str):
    if db.redis_connection is None:
        # Еще не создан - создайте
        db.redis_connection = redis.Redis(host=host, port=port, password=password, decode_responses=True)
    else:
        # Коннект уже почему то создан
        pass


def init_service(service_name, host, port):
    r = db.redis_connection
    replica_name = "replica_1"
    r.lpush(service_name, replica_name)
    r.hset(replica_name, "host", host)
    r.hset(replica_name, "port", port)


def init_scheduler(service_name: str):
    service_discover.discover(service_name=service_name)
    scheduler = APScheduler()
    scheduler.add_job(id='kek',
                      func=service_discover.discover(service_name=service_name),
                      trigger='interval', seconds=5)
    return scheduler
