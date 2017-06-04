from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..models import User
from .. import jwt

api = Blueprint('api', __name__)


@api.route('/')
@jwt_required
def protected():
    return '%s' % get_jwt_identity


@api.route('/sign_up', methods=['POST'])
def sign_up():
    conditions = [request.json.get('email', None), request.json.get('password', None)]

    if not all(conditions):
        return jsonify(message='Missing required data.'), 400

    user = User(
        email=conditions[0],
        password=conditions[1]
    ).create()

    if user:
        return jsonify(
            id=user.id,
            token=user.token
        )
    else:
        return jsonify(message='A user with the email %s already exists. Forgot your password?'), 400

@api.route('/sign_in', methods=['POST'])
def sign_in():
    conditions = [request.json.get('email', None), request.json.get('password', None)]

    if not all(conditions):
        return jsonify(message='Missing required data.'), 400

    user = User.validate_login(conditions[0], conditions[1])

    if user:
        return jsonify(token=user.token)
    else:
        return jsonify(message='Invalid login credentials'), 401