from flask import Blueprint, jsonify
from flask import request, jsonify
from flask_jwt_extended import create_access_token

blueprint = Blueprint('users', __name__)

@blueprint.route('/api/login', methods=('POST',))
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username and password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)