from marshmallow_mongoengine import ModelSchema  # To take advantage of ModelSchema with MongoEngine
from . import ma  # To take advantage of routing features of Flask-Marshmallow

from .models import Place, User

__all__ = [
    'PlaceSchema'
]


class PlaceSchema(ModelSchema):
    class Meta:
        model = Place

    url = ma.URLFor('api.place', id='<id>')


class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ('token',)
        exclude = ('_password', )

