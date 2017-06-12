import factory

from expert_tourist.models import Place, User, Route


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
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for place in extracted:
                self.places.append(place)