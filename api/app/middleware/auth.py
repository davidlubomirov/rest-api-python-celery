from flask import jsonify, request
from functools import wraps

import jwt

from app.env import SERVER_CONFIG


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "x-auth-token" in request.headers:
            token = request.headers["x-auth-token"]

        if not token:
            return jsonify(
                {
                    "msg": "Missing auth token"
                },
            ), 403

        try:
            decoded_data = jwt.decode(
                token, SERVER_CONFIG["JWT_SECRET"], algorithms=['HS256'])
        except:
            return jsonify(
                {
                    "msg": "Token is invalid"
                }
            ), 403

        return f(*args, **kwargs)

    return decorated
