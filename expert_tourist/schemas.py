from marshmallow import pre_load, pre_dump, post_dump, ValidationError
from marshmallow_mongoengine import ModelSchema  # To take advantage of ModelSchema with MongoEngine

from . import ma  # To take advantage of routing features of Flask-Marshmallow
from .models import Place, User, Route, Tourist
from .utils import convert_coordinates_to_point, convert_point_to_coordinates

__all__ = [
    'PlaceSchema', 'UserSchema', 'RouteSchema', 'TouristSchema'
]


class LocalizableMixin:
    @pre_load
    def deserialize_coordinates(self, data):
        if 'coordinates' not in data:
            raise ValidationError('Field <coordinates> is required')

        try:
            iter(data['coordinates'])
            data['coordinates'] = convert_coordinates_to_point(data['coordinates'])
            return data
        except:
            raise ValidationError('Field <coordinates> must be an iterable with two values')

    @post_dump
    def serialize_coordinates(self, data):
        data['coordinates'] = convert_point_to_coordinates(data['coordinates'])
        return data


class PlaceSchema(ModelSchema, LocalizableMixin):
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


class TouristSchema(ModelSchema, LocalizableMixin):
    class Meta:
        model = Tourist
