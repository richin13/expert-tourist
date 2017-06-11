import json

from faker import Faker
from expert_tourist import create_app
from expert_tourist.models import Place, PlaceDatasetManager, User
from flask_testing import TestCase
from .factories import UserFactory, PlaceFactory

json_str = """
  {
    "name": "Parque Acuático Cascada de Fuego",
    "area": 0,
    "price_range": 1,
    "category": "Balneario",
    "contact": "",
    "phone_number": "2276-6080",
    "email": "cascadadefuegoparqueacuatico@gmail.com",
    "region": "Valle Central",
    "location": "San José, Desamparados, Patarrá",
    "address": "2km sur de la iglesia de San Antonio de Desamparados, carretera a Patarra",
    "latitude": 9.8757875656828,
    "longitude": -84.03733452782035,
    "hours": "Lun-Dom: 8:00 am-5:00 pm"
  }
"""


class TestModels(TestCase):
    def create_app(self):
        app = create_app('config.TestConfig')
        return app

    def setUp(self):
        self.app = self.create_app().test_client()

    def tearDown(self):
        Place.drop_collection()
        User.drop_collection()

    def test_place_from_json(self):
        parsed_json = json.loads(json_str)
        place = Place(**parsed_json)
        str(place)

        self.assertEqual(place.name, 'Parque Acuático Cascada de Fuego')
        self.assertEqual(place.contact, '')
        self.assertEqual(place.price_range, 1)
        self.assertEqual(place.phone_number, '2276-6080')
        self.assertEqual('cascadadefuegoparqueacuatico@gmail.com', place.email)
        self.assertEqual(place.region, 'Valle Central')
        self.assertEqual(place.area, 0)
        self.assertEqual(place.location, 'San José, Desamparados, Patarrá')
        self.assertEqual(place.address, '2km sur de la iglesia de San Antonio de Desamparados, carretera a Patarra')
        self.assertEqual(place.google_maps, 'http://maps.google.co.cr/maps?q=9.8757875656828,-84.03733452782035')
        self.assertEqual(place.latitude, 9.8757875656828)
        self.assertEqual(place.longitude, -84.03733452782035)
        self.assertEqual(place.hours, 'Lun-Dom: 8:00 am-5:00 pm')
        self.assertEqual(place.category, 'Balneario')

    def test_place_loader(self):
        loader = PlaceDatasetManager()
        saved = loader.load_dataset()

        self.assertTrue(saved >= Place.objects.count())

    def test_data_group_by(self):
        loader = PlaceDatasetManager()
        grouped = loader.group_by('region')

        self.assertTrue(bool(grouped))

    def test_user_encrypted_password(self):
        user = UserFactory.build(password='abc123')
        json.dumps(user, cls=User.Encoder)

        self.assertNotEqual(user.password, 'abc123')

    def test_user_validate_valid_password(self):
        user = UserFactory.create(password='abc123')

        self.assertTrue(user.validate_password('abc123'))

        pass

    def test_user_validate_invalid_password(self):
        user = UserFactory.create(password='abc123')

        self.assertFalse(user.validate_password('123abc'))

    def test_user_with_encrypted_password_without_using_property(self):
        fake = Faker()
        password = fake.password()
        user = User(email=fake.email(), username=fake.user_name(), _password=password)

        self.assertNotEqual(password, user.password)

