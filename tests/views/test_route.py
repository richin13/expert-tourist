import json

from expert_tourist.models import Route, Tourist, Place, PlaceDatasetManager, TouristDatasetManager, TouristClassifier

from . import TestViewCase
from ..factories import RouteFactory, PlaceFactory, TouristFactory


class TestRouteResource(TestViewCase):
    def tearDown(self):
        Route.drop_collection()
        Tourist.drop_collection()
        Place.drop_collection()
        TouristClassifier.drop_collection()

    def test_get_all_routes(self):
        RouteFactory.create_batch(10, places=PlaceFactory.create_batch(3))

        res = self.app.get('/api/routes')

        self.assertEqual(res.status_code, 200)

    def test_paginated_routes(self):
        RouteFactory.create_batch(10, places=PlaceFactory.create_batch(3))
        res = self.app.get('/api/routes?paginate=1&page=1')

        self.assertEqual(res.status_code, 200)

    def test_get_one_existent_route(self):
        route = RouteFactory.create(places=PlaceFactory.create_batch(2))

        res = self.app.get('/api/routes/{}'.format(route.id))

        self.assertEqual(res.status_code, 200)

    def test_get_one_non_existent_route(self):
        res = self.app.get('/api/routes/{}'.format(self.fake.md5()[:24]))

        self.assertEqual(res.status_code, 404)

    def test_update_not_implemented(self):
        res = self.app.put(
            '/api/routes/{}'.format(self.fake.md5()[:24]),
            content_type='application/json',
            headers=self._authorize()
        )

        self.assertEqual(res.status_code, 501)

    def test_delete_not_implemented(self):
        res = self.app.delete(
            '/api/routes/{}'.format(self.fake.md5()[:24]),
            content_type='application/json',
            headers=self._authorize()
        )

        self.assertEqual(res.status_code, 501)

    def test_create_new_recommendation_without_places(self):
        tourist = TouristFactory.create()
        data = json.dumps(tourist, cls=Tourist.Encoder)

        res = self.app.post(
            '/api/recommend',
            content_type='application/json',
            data=data
        )

        self.assertEqual(res.status_code, 200)

    def test_create_recommendation_with_places(self):
        PlaceDatasetManager().load_dataset(Place)
        TouristDatasetManager().load_dataset(Tourist)

        for i in range(3):
            attrs = {
                "area": 0,
                "activity": 1,
                "budget": 1,
                "travel_dist": 2,
                "coordinates": [9.8408317, -83.8737972],
                "tourist_type": i
            }
            tourist = TouristFactory.create(**attrs)
            data = json.dumps(tourist, cls=Tourist.Encoder)

            res = self.app.post(
                '/api/recommend',
                content_type='application/json',
                data=data
            )

            self.assertEqual(res.status_code, 200)

    def test_create_new_recommendation_without_coords(self):
        tourist = TouristFactory.stub()
        tourist = {
            'vehicle': tourist.area,
            'budget': tourist.budget,
            'travel_dist': tourist.travel_dist,
            'activity': tourist.activity
        }

        data = json.dumps(tourist)
        res = self.app.post(
            '/api/recommend',
            content_type='application/json',
            data=data
        )

        self.assertEqual(res.status_code, 400)

    def test_create_new_recommendation_with_invalid_coords(self):
        tourist = TouristFactory.create()
        tourist.coordinates = []
        data = json.dumps(tourist, cls=Tourist.Encoder)
        res = self.app.post(
            '/api/recommend',
            content_type='application/json',
            data=data
        )

        self.assertEqual(res.status_code, 400)
