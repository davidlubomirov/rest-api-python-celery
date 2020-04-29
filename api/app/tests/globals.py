import base64

ROUTEST = {
    "login": "/api/login",
    "contact": "/api/contact"
}

HTTP_REQUIRED_HEADERS = {
    "Content-Type": "application/json"
}

TEST_INPUT = [
    {
        "username": "first_test_user",
        "first_name": "FirstFirstUser",
        "last_name": "LastFirstUser"
    },
    {
        "username": "second_test_user",
        "first_name": "FirstSecondUser",
        "last_name": "LastSecondUser"
    }
]


def build_basic_auth_header(username=None, password=None):
    if not username or not password:
        return ValueError("Invalid input parameters")

    return {
        'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')
    }
