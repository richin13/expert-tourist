from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_optional

from ..errors import APIException
from ..models import User

__all__ = ['AdministrativeResource']


class AdministrativeResource(Resource):
    @jwt_optional
    def _jwt_required(self):
        user_id = get_jwt_identity()
        if user_id is not None:
            if User.objects(id=user_id).first() is not None:
                return

        raise APIException('Missing authorization header', 401)

    def post(self):
        self._jwt_required()

    def put(self, id: str):
        self._jwt_required()

    def delete(self, id: str):
        self._jwt_required()
