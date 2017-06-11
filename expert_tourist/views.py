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
    schema = UserSchema().loads(request.data)

    if schema.errors:
        raise APIException('Fields <username, email, password> are required')

    user = schema.data
    if not user.exists():
        user.save()
        return jsonify(UserSchema().dump(user).data)
    else:
        raise APIException('A user with the email {} already exists. Forgot your password?'.format(user.email))


@api.route('/sign_in', methods=['POST'])
def sign_in():
    conditions = [request.json.get('username', None), request.json.get('password', None)]

    if not all(conditions):
        raise APIException('Fields <username, password> are required.')

    user = User.validate_login(conditions[0], conditions[1])

    if user:
        return jsonify(UserSchema().dump(user).data)
    else:
        raise APIException('Invalid login credentials', status_code=401)
