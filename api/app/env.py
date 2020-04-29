import os
import sys

SERVER_CONFIG = {}
REQUIRED_VARIABLES = [
    "REDIS_BROCKER_URL",
    "SQLITE_FILE_NAME",
    "JWT_SECRET",
    "API_AUTH_USERNAME",
    "API_AUTH_PASSWORD"
]


def parse_env_variables():
    for each_env_var in REQUIRED_VARIABLES:
        if os.getenv(each_env_var) is None:
            print("Missing environment configuration: {}".format(each_env_var))
            sys.exit(1)

        SERVER_CONFIG[each_env_var] = os.getenv(each_env_var)
