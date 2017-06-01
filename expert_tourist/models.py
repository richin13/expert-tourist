from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.hybrid import hybrid_property

from . import bcrypt

db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())


class User(BaseModel):
    email = db.Column(db.String(64), unique=True)
    _password = db.Column(db.String(64))

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, pw):
        self._password = bcrypt.generate_password_hash(pw)

    def validate_password(self, password):
        return bcrypt.check_password_hash(bytes(self.password), password)

    @staticmethod
    def validate_login(email, password):
        print(email)
        user: User = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return None

    @staticmethod
    def identity(payload):
        print(str(payload))
        return User.query.get(payload['identity'])

    def create(self):
        db.session.add(self)

        try:
            db.session.commit()

            return User.query.filter_by(email=self.email).first()
        except IntegrityError:
            return None

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        return create_access_token(identity=self.id)
