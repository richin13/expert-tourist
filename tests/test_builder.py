from flask_testing import TestCase

from expert_tourist import create_app

from expert_tourist.builder import RouteBuilder
from expert_tourist.models import Tourist, Place, Route

from .factories import PlaceFactory


class TestRouteBuilder(TestCase):
    def create_app(self):
        app = create_app('config.TestConfig')
        return app

    def setUp(self):
        self.app = self.create_app().test_client()
        attrs = {
            "area": 0,
            "activity": 1,
            "budget": 1,
            "travel_dist": 2,
            "coordinates": [9.8408317, -83.8737972],
            "tourist_type": 1
        }
        self.builder = RouteBuilder(Tourist(**attrs))

    def tearDown(self):
        Tourist.drop_collection()
        Place.drop_collection()
        Route.drop_collection()
        del self.builder

    def test_build_path_without_places(self):
        path = self.builder._build_path([])
        self.assertIsNone(path)

    def test_build_path_with_one_place(self):
        place = PlaceFactory.create()
        path = self.builder._build_path([(place,0)])
        self.assertEqual(path, [place])
