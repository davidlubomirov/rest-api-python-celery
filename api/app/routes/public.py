from flask import Blueprint, jsonify, request

import jwt
import datetime

from app.subtasks.contact import create_random_contacts
from app.env import SERVER_CONFIG

public_api_bp = Blueprint("public", __name__)


@public_api_bp.route("/api/status", methods=["GET"])
def status_check():
    return jsonify({"msg": "service is up and running"}), 200


@public_api_bp.route("/api/login", methods=["POST"])
def login():
    auth = request.authorization

    if auth is None:
        return jsonify(
            {
                "msg": "Invalid auth"
            }
        ), 400

    if auth.username != SERVER_CONFIG["API_AUTH_USERNAME"] or auth.password != SERVER_CONFIG["API_AUTH_PASSWORD"]:
        return jsonify(
            {
                "msg": "Invalid username or password"
            }
        ), 403

    expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    token = jwt.encode(
        {
            "exp": expiration
        },
        SERVER_CONFIG["JWT_SECRET"]
    )

    return jsonify(
        {
            "token": token.decode("UTF-8")
        }
    ), 200
