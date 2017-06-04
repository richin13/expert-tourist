import os
import yaml

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.hybrid import hybrid_property

from .utils import gmaps_url_to_coords
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


categories = db.Table('place_category_many_to_many',
                      db.Column('place_id', db.Integer, db.ForeignKey('place.id')),
                      db.Column('place_category_id', db.Integer, db.ForeignKey('place_category.id'))
                      )


class Place(BaseModel):
    name = db.Column(db.String(64))
    contact = db.Column(db.String(32))
    phone_number = db.Column(db.String(32))
    email = db.Column(db.String(64))
    facebook = db.Column(db.String(128))
    region = db.Column(db.String(32))
    area = db.Column(db.String(32))
    location = db.Column(db.String(64))
    address = db.Column(db.String(128))
    google_maps = db.Column(db.String(80))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    hours = db.Column(db.String(32))

    # Many to many with category
    categories = db.relationship('PlaceCategory', secondary=categories,
                                 backref=db.backref('places', lazy='dynamic'))

    @staticmethod
    def from_yml(yml: dict):
        """
        Converts a YAML-like python dict with a data for a given place.
        
        :param yml: YAML-like python dict with the data of a place for a given YAML record in the dataset.
        :return: A tuple with a newly-created Place with the attributes given as function argument
        and a Generator of PlaceCategory with all the categories of the place
        """
        name, = yml.keys()
        attrs = yml[name]
        lat, long = gmaps_url_to_coords(attrs.get('google_maps', ''))

        # Categories generator
        categories_ = PlaceCategory.from_messed_type(attrs['type'])
        del attrs['type']

        return Place(name=name, latitude=lat, longitude=long, **attrs), categories_


class PlaceCategory(BaseModel):
    name = db.Column(db.String(80), unique=True)

    # Warning: nasty line incoming...
    known_categories = ['Balneario / Piscina',
                        'Área Verde / Parque Municipal',
                        'Catarata & Cascada',
                        'Senderos / Caminata',
                        'Lago & Laguna',
                        'Centro de Recreación',
                        'Escalar',
                        'Parque Temático',
                        'Granja / Finca',
                        'Tour a Caballo / Cabalgata',
                        'Aguas Termales',
                        'Aguas Temperadas',
                        'Playa',
                        'Pesca Deportiva',
                        'Surf',
                        'Canopy',
                        'Campamento',
                        'Futbol',
                        'Historia / Cultural',
                        'Restaurante',
                        'Soda',
                        'Iglesia',
                        'Fisioterapia / Rehabilitación',
                        'Estética',
                        'Cabañas',
                        'Caminata',
                        'Refugio de Vida Silvestre',
                        'Corredor Biológico',
                        'Bar',
                        'Galería de Arte',
                        'Teatro',
                        'Cine',
                        'Hotel',
                        'Universidad',
                        'Cabina',
                        'Mariposario',
                        'Hospital',
                        'Mirador',
                        'Cerro / Montaña',
                        'Museo',
                        'Centro Comercial',
                        'Zoológico',
                        'Área Silvestre Protegida',
                        'Reserva Biológica',
                        'Zona Protectora',
                        'Cavernas / Cuevas',
                        'Área de Conservación',
                        'Jardín Botánico',
                        'Volcán',
                        'Rescate / Conservación Animal',
                        'Reserva Privada',
                        'Complejo Turístico',
                        'Picnic',
                        'Autobús']

    @staticmethod
    def from_messed_type(type):
        # Note we're yielding newly-created categories and that
        # name is set to be a unique attribute.
        # Should we check if the category already exists?
        fitted_in_category = False
        for category in PlaceCategory.known_categories:  # this
            if category in type:  # plus this, it's a costly operation (even for a super awesome language like python)
                fitted_in_category = True
                yield PlaceCategory(name=category)
        if not fitted_in_category:
            yield PlaceCategory(name=type)  # Fallback

    @staticmethod
    def exists(name):
        return PlaceCategory.query.filter_by(name=name).first()

    def __str__(self):
        return '{}'.format(self.name)


class PlaceLoader:
    data_source_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../', 'data', 'places.yml')
    data_source = None

    def __init__(self):
        if os.path.isfile(self.data_source_path):
            with open(self.data_source_path, 'r') as f:
                self.data_source = yaml.load(f)

    def to_db(self):
        if self.data_source:
            for yml in self.data_source:
                place, categories_ = Place.from_yml(yml)
                for category in categories_:
                    existing = PlaceCategory.exists(category.name)
                    if existing:
                        place.categories.append(existing)
                    else:
                        place.categories.append(category)
                db.session.add(place)
            db.session.commit()
        else:
            raise AttributeError('Error loading data source')

        print('DONE')
