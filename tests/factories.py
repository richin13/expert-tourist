import factory
from factory.fuzzy import FuzzyInteger, FuzzyChoice

from expert_tourist.models import Place, User, Route, Tourist


class PlaceFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = Place

    name = factory.Faker('company')
    area = FuzzyChoice([0,1,2])
    price_range = FuzzyChoice([0,1,2])
    activities = FuzzyChoice([0,1,2])
    category = factory.Faker('first_name')
    contact = factory.Faker('first_name')
    phone_number = factory.Faker('phone_number')
    email = factory.Faker('email')
    region = factory.Faker('city')
    location = factory.Faker('city')
    address = factory.Faker('address')
    hours = 'Lun-Dom 8:00-17:00'
    # latitude = factory.Faker('latitude')
    # longitude = factory.Faker('longitude')
    coordinates = [9.933567, -84.077023]#factory.LazyAttribute(lambda o: [float(o.latitude), float(o.longitude)])
    google_maps = factory.LazyAttribute(
        lambda obj: 'http://maps.google.co.cr/maps?q=%f,%f' % (obj.coordinates[0], obj.coordinates[1]))
    place_type = FuzzyChoice([0,1,2])
    created_at = factory.Faker('date_time')


class UserFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = User

    email = factory.Faker('email')
    username = factory.Faker('user_name')
    password = factory.Faker('password')


class RouteFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = Route

    places = factory.List([])
    tourist_type = FuzzyChoice([0, 1, 2])


class TouristFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = Tourist

    area = FuzzyInteger(0, 2)
    budget = FuzzyInteger(0, 2)
    travel_dist = FuzzyInteger(0, 2)
    activity = FuzzyInteger(0, 2)
    tourist_type = FuzzyInteger(0, 2)
    coordinates = [9.933567, -84.077023]
