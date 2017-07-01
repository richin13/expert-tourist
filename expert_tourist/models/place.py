import json
import mongoengine as me
from datetime import datetime
from geopy.distance import EARTH_RADIUS

from . import db, DatasetManager
from ..utils import coords_to_gmaps_url, AREA_ENCODING, PRICE_ENCODING, ACTIVITIES_ENCODING, CLASSES_ENCODING
from ..utils import travel_distances, budget_limits


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
    area = me.IntField(required=True, choices=AREA_ENCODING)
    price_range = me.IntField(required=True, choices=PRICE_ENCODING)
    activities = me.IntField(required=True, choices=ACTIVITIES_ENCODING)
    category = me.StringField(max_length=64, required=True)
    contact = me.StringField(max_length=128)
    phone_number = me.StringField(max_length=128)
    email = me.EmailField(max_length=64, null=True)
    region = me.StringField(max_length=128)
    location = me.StringField(max_length=128)
    address = me.StringField(max_length=500)
    google_maps = me.StringField(max_length=80)
    hours = me.StringField(max_length=128)
    coordinates = me.PointField(required=True)
    place_type = me.IntField(required=True, choices=CLASSES_ENCODING)
    created_at = me.DateTimeField()

    def __init__(self, *args, **kwargs):
        super(Place, self).__init__(*args, **kwargs)

        self.created_at = datetime.now()
        emails = kwargs.get('email', '').split(', ')[0]  # Take just the first email

        self.email = emails if len(emails) > 0 else None

        google_maps = kwargs.get('google_maps', None)
        if not bool(google_maps):  # Check whether it is null or empty
            self.google_maps = coords_to_gmaps_url(self.coordinates[0], self.coordinates[1])

    def __str__(self):
        return 'Place<%s, %s>' % (self.name, self.category)

    @staticmethod
    def find_for(tourist):
        pipeline = Place._build_pipeline(tourist)
        places_raw = Place.objects.aggregate(*pipeline)
        places = list()

        for place_raw in places_raw:
            place_raw['id'] = place_raw.pop('_id')
            dist_to_tourist = place_raw.pop('dist_to_tourist')
            places.append((Place(**place_raw), dist_to_tourist))

        return places

    @staticmethod
    def _build_filters(tourist):
        max_distance = travel_distances[tourist.travel_dist]
        budget = tourist.budget
        limit = budget_limits[budget]

        return max_distance, limit

    @staticmethod
    def _build_pipeline(tourist):
        max_distance, limit = Place._build_filters(tourist)
        pipeline = list()
        geo_near = {'$geoNear': {'near': tourist.coordinates, 'distanceField': 'dist_to_tourist',
                                 'distanceMultiplier': EARTH_RADIUS * 10 ** -6, 'spherical': True}}
        pipeline.append(geo_near)

        match = {'$match': {'place_type': tourist.tourist_type, 'dist_to_tourist': {'$lte': max_distance}}}
        pipeline.append(match)

        sort = {'$sort': {'dist_to_tourist': 1}}
        pipeline.append(sort)

        return pipeline

    class Encoder(json.encoder.JSONEncoder):
        def encode(self, o):
            if type(o) == Place:
                o = {
                    'name': o.name,
                    'area': o.area,
                    'price_range': o.price_range,
                    'activities': o.activities,
                    'category': o.category,
                    'contact': o.contact,
                    'phone_number': o.phone_number,
                    'email': o.email,
                    'region': o.region,
                    'location': o.location,
                    'address': o.address,
                    'google_maps': o.google_maps,
                    'hours': o.hours,
                    'coordinates': o.coordinates,
                    'place_type': o.place_type,
                    'created_at': o.created_at.isoformat(),
                }

            return super(Place.Encoder, self).encode(o)


class PlaceDatasetManager(DatasetManager):
    filename = 'places.json'
