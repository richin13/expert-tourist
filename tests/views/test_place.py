import json

from expert_tourist.models import Place

from . import TestViewCase
from ..factories import PlaceFactory


class TestPlaceResource(TestViewCase):
    def tearDown(self):
        Place.drop_collection()

    def test_get_all_places(self):
        places = self.app.get('/api/places')

        self.assertEqual(places.status_code, 200)

    def test_get_paginated_places(self):
        places = self.app.get('/api/places?paginate=1&page=1')

        self.assertEqual(places.status_code, 200)

    def test_get_one_place(self):
        place = PlaceFactory.create()

        retrieved_place = self.app.get('/api/places/{}'.format(place.id))

        self.assertEqual(200, retrieved_place.status_code)

    def test_get_one_nonexistent_place(self):
        retrieved_place = self.app.get('/api/places/{}'.format(self.fake.md5()[:24]))

        self.assertEqual(404, retrieved_place.status_code)

    def test_insert_one_place_without_authorization(self):
        place = PlaceFactory.build()
        data = json.dumps(place, cls=Place.Encoder)

        saved_place = self.app.post(
            '/api/places',
            data=data,
            content_type='application/json'
        )

        self.assertEqual(401, saved_place.status_code)

    def test_insert_one_place_with_authorization(self):
        place = PlaceFactory.build()
        data = json.dumps(place, cls=Place.Encoder)

        saved_place = self.app.post(
            '/api/places',
            data=data,
            content_type='application/json',
            headers=self._authorize()
        )

        self.assertEqual(201, saved_place.status_code)

    def test_insert_bad_place(self):
        place = PlaceFactory.build()
        place.name = None
        data = json.dumps(place, cls=Place.Encoder)

        saved_place = self.app.post(
            '/api/places',
            data=data,
            content_type='application/json',
            headers=self._authorize()
        )

        self.assertEqual(400, saved_place.status_code)

    def test_update_place_with_authorization(self):
        place = PlaceFactory.create()
        place.name = 'New super awesome name'  # Update the created place
        data = json.dumps(place, cls=Place.Encoder)

        updated_place = self.app.put(
            '/api/places/{}'.format(place.id),
            data=data,
            content_type='application/json',
            headers=self._authorize()
        )

        data = json.loads(updated_place.data)

        self.assertEqual(updated_place.status_code, 200)
        self.assertEqual(data['name'], 'New super awesome name')

    def test_update_place_without_authorization(self):
        place = PlaceFactory.create()

        updated_place = self.app.put(
            '/api/places/{}'.format(place.id),
            content_type='application/json'
        )

        self.assertEqual(updated_place.status_code, 401)

    def test_delete_place_with_authorization(self):
        place = PlaceFactory.create()

        deleted_place = self.app.delete(
            '/api/places/{}'.format(place.id),
            content_type='application/json',
            headers=self._authorize()
        )

        self.assertEqual(deleted_place.status_code, 204)

    def test_delete_place_without_authorization(self):
        place = PlaceFactory.create()

        deleted_place = self.app.delete(
            '/api/places/{}'.format(place.id),
            content_type='application/json'
        )

        self.assertEqual(deleted_place.status_code, 401)
