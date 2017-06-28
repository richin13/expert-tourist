import json

from flask_testing import TestCase

from expert_tourist import create_app
from expert_tourist.models import Place, Tourist, PlaceDatasetManager

from ..factories import PlaceFactory, TouristFactory

json_str = """
  {
    "name": "Parque Acuático Cascada de Fuego",
    "area": 0,
    "price_range": 1,
    "activities": 0,
    "category": "Balneario",
    "contact": "",
    "phone_number": "2276-6080",
    "email": "cascadadefuegoparqueacuatico@gmail.com",
    "region": "Valle Central",
    "location": "San José, Desamparados, Patarrá",
    "address": "2km sur de la iglesia de San Antonio de Desamparados, carretera a Patarra",
    "coordinates": [9.8757875656828, -84.03733452782035],
    "place_type": 1,
    "hours": "Lun-Dom: 8:00 am-5:00 pm"
  }
"""
SHORT_DIST = 0
MEDIUM_DIST = 1
LONG_DIST = 2


class TestPlaceModel(TestCase):
    def create_app(self):
        app = create_app('config.TestConfig')
        return app

    def setUp(self):
        self.app = self.create_app().test_client()

    def tearDown(self):
        Place.drop_collection()
        Tourist.drop_collection()

    def test_place_from_json(self):
        parsed_json = json.loads(json_str)
        place = Place(**parsed_json)
        str(place)

        self.assertEqual(place.name, 'Parque Acuático Cascada de Fuego')
        self.assertEqual(place.contact, '')
        self.assertEqual(place.price_range, 1)
        self.assertEqual(place.activities, 0)
        self.assertEqual(place.phone_number, '2276-6080')
        self.assertEqual('cascadadefuegoparqueacuatico@gmail.com', place.email)
        self.assertEqual(place.region, 'Valle Central')
        self.assertEqual(place.area, 0)
        self.assertEqual(place.location, 'San José, Desamparados, Patarrá')
        self.assertEqual(place.address, '2km sur de la iglesia de San Antonio de Desamparados, carretera a Patarra')
        self.assertEqual(place.google_maps, 'http://maps.google.co.cr/maps?q=9.8757875656828,-84.03733452782035')
        self.assertEqual(place.coordinates, [9.8757875656828, -84.03733452782035])
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

    def test_find_places_for_tourist_within_short_distance(self):
        t = TouristFactory.create(coordinates=[9.836097, -83.715022], travel_dist=SHORT_DIST)

        PlaceFactory.create(coordinates=[10.054347222222223, -84.27854722222222],
                            place_type=t.tourist_type)  # Somewhere in Alajuela
        PlaceFactory.create(coordinates=[9.783058419314655, -83.68817796930671],
                            place_type=t.tourist_type)  # La Marta (you should visit here, btw)
        PlaceFactory.create(coordinates=[9.596189, -84.618088], place_type=t.tourist_type)  # Jaco

        self.assertEqual(len(Place.find_for(t)), 1)

    def test_find_places_for_tourist_within_medium_distance(self):
        t = TouristFactory.create(coordinates=[9.836097, -83.715022], travel_dist=MEDIUM_DIST)

        PlaceFactory.create(coordinates=[10.054347222222223, -84.27854722222222],
                            place_type=t.tourist_type)  # Somewhere in Alajuela
        PlaceFactory.create(coordinates=[9.783058419314655, -83.68817796930671],
                            place_type=t.tourist_type)  # La Marta (you should visit here, btw)
        PlaceFactory.create(coordinates=[9.596189, -84.618088], place_type=t.tourist_type)  # Jaco

        self.assertEqual(len(Place.find_for(t)), 2)

    def test_find_places_for_tourist_within_long_distance(self):
        t = TouristFactory.create(coordinates=[9.836097, -83.715022], travel_dist=LONG_DIST)

        PlaceFactory.create(coordinates=[10.054347222222223, -84.27854722222222],
                            place_type=t.tourist_type)  # Somewhere in Alajuela
        PlaceFactory.create(coordinates=[9.783058419314655, -83.68817796930671],
                            place_type=t.tourist_type)  # La Marta (you should visit here, btw)
        PlaceFactory.create(coordinates=[9.596189, -84.618088], place_type=t.tourist_type)  # Jaco

        self.assertEqual(len(Place.find_for(t)), 3)
