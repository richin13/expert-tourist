from expert_tourist.models import Route

from . import TestViewCase
from ..factories import RouteFactory, PlaceFactory


class TestRouteResource(TestViewCase):
    def tearDown(self):
        Route.drop_collection()

    def test_get_all_routes(self):
        RouteFactory.create_batch(10)

        res = self.app.get('/api/routes')

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