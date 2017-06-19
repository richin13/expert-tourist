import json

from flask_testing import TestCase

from expert_tourist import create_app
from expert_tourist.models import Place, Classifier, PlaceDatasetManager

from ..factories import PlaceFactory

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


class TestPlaceModel(TestCase):
    def create_app(self):
        app = create_app('config.TestConfig')
        return app

    def setUp(self):
        self.app = self.create_app().test_client()

    def tearDown(self):
        Place.drop_collection()

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
        saved = loader.load_dataset(Place)

        self.assertTrue(saved >= Place.objects.count())

    def test_data_group_by(self):
        loader = PlaceDatasetManager()
        grouped = loader.group_by('region')

        self.assertTrue(bool(grouped))
