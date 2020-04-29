import os
import sys

from flask import Flask

from .celery_utils import init_celery

PACKAGE_NAME = os.path.dirname(os.path.realpath(__file__)).split("/")[-1]
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

REQUIRED_VARS = [
    "REDIS_BROCKER_URL",
    "SQLITE_FILE_NAME"
]
SERVER_CONFIG = {}


def _parse_env_variables():
    for each_env_var in REQUIRED_VARS:
        if os.getenv(each_env_var) is None:
            print("Unable to validate variable: {}".format(each_env_var))

            sys.exit(1)

        SERVER_CONFIG[each_env_var] = os.getenv(each_env_var)


def create_app(app_name=PACKAGE_NAME, **kwargs):
    _parse_env_variables()

    app = Flask(app_name)

    if kwargs.get("celery"):
        init_celery(kwargs.get("celery"), app)

    from app.routes.contact import contact_api
    from app.routes.public import public_api_bp

    from app.db import db, ma

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///{}".format(
        os.path.join(BASE_DIR, SERVER_CONFIG["SQLITE_FILE_NAME"])
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.app_context().push()
    db.init_app(app)
    ma.init_app(app)

    if not os.path.exists(os.path.join(BASE_DIR, SERVER_CONFIG["SQLITE_FILE_NAME"])):
        from app.models.contact import Contact, Email
        db.create_all()

    app.register_blueprint(contact_api)
    app.register_blueprint(public_api_bp)

    return app
