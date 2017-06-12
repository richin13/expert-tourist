from marshmallow import pre_load, post_dump, ValidationError
from marshmallow_mongoengine import ModelSchema  # To take advantage of ModelSchema with MongoEngine

from . import ma  # To take advantage of routing features of Flask-Marshmallow
from .models import Place, User, Route, Tourist

__all__ = [
    'PlaceSchema', 'UserSchema', 'RouteSchema', 'TouristSchema'
]


class PlaceSchema(ModelSchema):
    class Meta:
        model = Place

    url = ma.URLFor('api.place', id='<id>')


class UserSchema(ModelSchema):
    class Meta:
        model = User

    @pre_load
    def include_password_property(self, in_data):
        if 'password' not in in_data:
            raise ValidationError('Field <password> is required')

        in_data['_password'] = in_data['password']

        return in_data

    @post_dump
    def include_token_property(self, data):
        user = self._make_object(data)
        data.pop('_password', '')  # Do not expose encrypted password in JSON response
        data['token'] = user.token  # Include the user's token

        return data


class RouteSchema(ModelSchema):
    class Meta:
        model = Route


class TouristSchema(ModelSchema):
    class Meta:
        model = Tourist
