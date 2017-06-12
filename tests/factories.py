import factory
import random

from expert_tourist.models import Place, User, Route, Tourist


class PlaceFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = Place

    name = factory.Faker('company')
    area = 0
    price_range = 0
    category = factory.Faker('first_name')
    contact = factory.Faker('first_name')
    phone_number = factory.Faker('phone_number')
    email = factory.Faker('email')
    region = factory.Faker('city')
    location = factory.Faker('city')
    address = factory.Faker('address')
    hours = 'Lun-Dom 8:00-17:00'
    latitude = factory.Faker('latitude')
    longitude = factory.Faker('longitude')
    google_maps = factory.LazyAttribute(
        lambda obj: 'http://maps.google.co.cr/maps?q=%f,%f' % (obj.latitude, obj.longitude))
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

    @factory.post_generation
    def places(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for place in extracted:
                self.places.append(place)


class TouristFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = Tourist

    vehicle = random.randint(0, 3)
    budget = random.randint(0, 3)
    travel_dist = random.randint(0, 3)
    activity = random.randint(0, 3)
    tourist_type = 'Unlabeled'
    latitude = 9.933567
    longitude = -84.077023