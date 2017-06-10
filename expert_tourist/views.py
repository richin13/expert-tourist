from collections import namedtuple

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from .models import User
from .errors import APIException
from .schemas import UserSchema

api = Blueprint('api', __name__)


@api.route('/whoami')
@jwt_required
def protected():
    return jsonify(token=get_jwt_identity())


@api.route('/sign_up', methods=['POST'])
def sign_up():
    Conditions = namedtuple('Conditions', 'username email password')
    conditions = Conditions(
        request.json.get('username', None),
        request.json.get('email', None),
        request.json.get('password', None)
    )

    if not all(conditions):
        raise APIException('Fields <username, email, password> are required')

    user = User(
        username=conditions.username,
        email=conditions.email,
        password=conditions.password,
    ).save()

    if user:
        return jsonify(UserSchema().dump(user).data)
    else:
        raise APIException('A user with the email {} already exists. Forgot your password?'.format(conditions[1]))


@api.route('/sign_in', methods=['POST'])
def sign_in():
    conditions = [request.json.get('username', None), request.json.get('password', None)]

    if not all(conditions):
        raise APIException('Fields username and password are required.')

    user = User.validate_login(conditions[0], conditions[1])

    if user:
        print(user.token)
        return jsonify(token=user.token)
    else:
        raise APIException('Invalid login credentials', status_code=401)
