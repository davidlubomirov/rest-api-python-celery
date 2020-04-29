from celery import Celery

from app.env import parse_env_variables, SERVER_CONFIG


def make_celery(app_name=__name__):
    parse_env_variables()

    backend = "{}/0".format(SERVER_CONFIG["REDIS_BROCKER_URL"])
    broker = backend.replace("0", "1")

    return Celery(app_name, backend=backend, broker=broker)


celery = make_celery()
