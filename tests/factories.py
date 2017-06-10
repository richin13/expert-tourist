import factory

from expert_tourist.models import Place, User


class PlaceFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = Place

    name = factory.Faker('company')
    area = factory.Faker('name')
    price_range = 'Cheap'
    category = factory.Faker('first_name')
    contact = factory.Faker('first_name')
    phone_number = factory.Faker('phone_number')
    email = factory.Faker('email')
    region = factory.Faker('city')
    location = factory.Faker('city')
    address = factory.Faker('address')
    google_maps = 'http://maps.google.co.cr/maps?q=9.8757875656828,-84.03733452782035'
    hours = 'Lun-Dom 8:00-17:00'
    latitude = factory.Faker('latitude')
    longitude = factory.Faker('longitude')
    created_at = factory.Faker('date_time')


class UserFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = User

    email = factory.Faker('email')
    username = factory.Faker('user_name')
    password = factory.Faker('password')