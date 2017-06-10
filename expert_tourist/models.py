import os
import json
from datetime import datetime

import mongoengine as me
from flask import current_app
from flask_jwt_extended import create_access_token
from flask_mongoengine import MongoEngine

from .utils import gmaps_url_to_coords
from . import bcrypt

db = MongoEngine()


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


class Place(db.Document):
    """
    Representation of a touristic place with all its properties. This will allow more flexibility when
    calculating new routes and will also work as a Wrapper for PyMongo.

    A physical place contains a set of attributes described as follows:

    Name:
        The common name used to tell different places apart. It will probably be the branding name of the place.

    Area:
        The geographic area where the place is located in terms of type of terrain or location. Some examples are:
            - Mountain
            - Beach
            - Rural
            - City
            - Etc.

    Price range:
        A general classification of how much money will take to visit this place. Can take any value in the following
        set:
            - Free
            - Cheap
            - Moderate
            - Expensive

    Category:
        The category of the place. This can take a value in a wide range of pre-set values. Some examples are:
            - Beach
            - Hotel
            - Restaurant
            - Cinema
            - Etc...

    Contact:
        Some places contains information on who to contact in order to visit the place. This field is dedicated to them.

    Phone number:
        The phone number of the place (Bet you did not see this coming)

    Email:
        The email of the place.

    Region:
        Our country is often separated into different regions which are Central Valley, Caribbean, Central Pacific, etc.
        This field refers to the country's region where the place is located.

    Location:
        The political location of the place. Say Province, Canton, District.

    Address:
        A hand-crafted and tico-version address of the exact location of the place.

    Google Maps:
        URL to Google Map's place location

    Latitude:
        The latitude where the place is located.

    Longitude:
        The longitude where the place is located.

    Hours:
        The opening hours of the place.

    Provide each attribute as a keyword argument in the constructor's call. Attributes such as Latitude and Longitude
    will be automatically guessed if they are missing from the constructor's call.

    """

    # Fields
    name = me.StringField(max_length=128, required=True)
    area = me.StringField(max_length=128, required=True)
    price_range = me.StringField(max_length=32, required=True)
    category = me.StringField(max_length=64, required=True)
    contact = me.StringField(max_length=128)
    phone_number = me.StringField(max_length=128)
    email = me.EmailField(max_length=64, null=True)
    region = me.StringField(max_length=128)
    location = me.StringField(max_length=128)
    address = me.StringField(max_length=500)
    google_maps = me.StringField(max_length=80, required=True)
    hours = me.StringField(max_length=128)
    latitude = me.FloatField()
    longitude = me.FloatField()
    created_at = me.DateTimeField()

    def __init__(self, *args, **kwargs):
        super(Place, self).__init__(*args, **kwargs)

        self.created_at = datetime.now()
        emails = kwargs.get('email', '').split(', ')[0]  # Take just the first email

        self.email = emails if len(emails) > 0 else None

        # Calculate latitude and longitude, if none given.
        google_maps = kwargs.get('google_maps', '')
        if not all([kwargs.get('latitude', None), kwargs.get('longitude', None)]) and google_maps:
            self.latitude, self.longitude = gmaps_url_to_coords(google_maps)

    def __str__(self):
        return 'Place<%s, %s>' % (self.name, self.category)

    class Encoder(json.encoder.JSONEncoder):
        def encode(self, o):
            if type(o) == Place:
                o = {
                    'name': o.name,
                    'area': o.area,
                    'price_range': o.price_range,
                    'category': o.category,
                    'contact': o.contact,
                    'phone_number': o.phone_number,
                    'email': o.email,
                    'region': o.region,
                    'location': o.location,
                    'address': o.address,
                    'google_maps': o.google_maps,
                    'hours': o.hours,
                    'latitude': o.latitude,
                    'longitude': o.longitude,
                    'created_at': o.created_at.isoformat(),
                }

            return super(Place.Encoder, self).encode(o)


class PlaceLoader:
    data_source_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../', 'data', 'places.json')
    data_source = None

    def __init__(self):
        if os.path.isfile(self.data_source_path):
            with open(self.data_source_path, 'r') as f:
                self.data_source = json.loads(f.read())

    def to_db(self):
        print('Loading data in {}'.format(current_app.config.get('MONGODB_SETTINGS', {'db': 'NONE'})['db']))
        saved_places_count = 0
        if self.data_source:
            for raw_place in self.data_source:
                place = Place(**raw_place)
                place.save()
            saved_places_count = len(self.data_source)
            print('[Done]', end=' ')

        print('Saved a total of {} places'.format(saved_places_count))
        return saved_places_count