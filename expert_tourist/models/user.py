import json
import mongoengine as me
from flask_jwt_extended import create_access_token

from . import db
from .. import bcrypt


class User(db.Document):
    email = me.EmailField(max_length=64, required=True)
    username = me.StringField(max_length=32, required=True)
    _password = me.StringField(max_length=128, required=True, db_field='password')

    def __init__(self, *args, **kwargs):
        password = kwargs.pop('password', None)
        super(db.Document, self).__init__(*args, **kwargs)

        if password:
            self.password = password

    def _get_password(self):
        return self._password.encode()

    def _set_password(self, clear_password):
        self._password = bcrypt.generate_password_hash(clear_password).decode('utf-8')

    password = property(_get_password, _set_password)

    def validate_password(self, password):
        return bcrypt.check_password_hash(bytes(self.password), password)

    @staticmethod
    def validate_login(username, password):
        user = User.objects(username=username).first()

        if user and user.validate_password(password):
            return user
        else:
            return None

    def exists(self):
        return User.objects(email=self.email).first() != None

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        return create_access_token(identity=str(self.id))

    class Encoder(json.encoder.JSONEncoder):
        def encode(self, o):
            if type(o) == User:
                o = {
                    'id': str(o.id),
                    'email': o.email,
                    'username': o.username,
                    'password': o.password.decode('utf-8'),
                }

            return super(User.Encoder, self).encode(o)
