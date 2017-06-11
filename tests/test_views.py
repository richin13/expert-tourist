import json

from expert_tourist import create_app
from expert_tourist.models import Place, User
from flask_testing import TestCase
from faker import Faker

from .factories import PlaceFactory, UserFactory


class TestAPI(TestCase):
    def create_app(self):
        app = create_app('config.TestConfig')
        app.config['MONGODB_SETTINGS'] = {
            'db': 'test'
        }
        return app

    def setUp(self):
        self.app = self.create_app().test_client()

    def tearDown(self):
        Place.drop_collection()
        User.drop_collection()

    def _authorize(self):
        user = UserFactory.create()
        return {'Authorization': user.token}

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
        retrieved_place = self.app.get('/api/places/{}'.format(Faker().md5()[:24]))

        self.assertEqual(404, retrieved_place.status_code)

    def test_insert_one_place_without_authorization(self):
        place = PlaceFactory.build()
        data = json.dumps(place, cls=Place.Encoder)
        print(data, type(data))
        saved_place = self.app.post(
            '/api/places',
            data=data,
            content_type='application/json'
        )

        self.assertEqual(401, saved_place.status_code)

    def test_insert_one_place_with_authorization(self):
        place = PlaceFactory.build()
        data = json.dumps(place, cls=Place.Encoder)
        print(data, type(data))
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
        place.name = 'New super awesome name' # Update the created place
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

        self.assertEqual(deleted_place.status_code, 200)

    def test_delete_place_without_authorization(self):
        place = PlaceFactory.create()

        deleted_place = self.app.delete(
            '/api/places/{}'.format(place.id),
            content_type='application/json'
        )

        self.assertEqual(deleted_place.status_code, 401)

    def test_sign_up_with_valid_data(self):
        random_user = UserFactory.build()
        sign_up_details = {
            'username': random_user.username,
            'email': random_user.email,
            'password': Faker().password()
        }

        res = self.app.post(
            "/api/sign_up",
            data=json.dumps(sign_up_details),
            content_type='application/json'
        )

        res_data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(res_data.get('token', None))
        self.assertIsNotNone(User.objects(email=random_user.email))  # Was it created?

    def test_sign_up_with_missing_data(self):
        random_user = UserFactory.build()
        sign_up_details = {
            'username': random_user.username,
            'email': random_user.email,
        }

        res = self.app.post(
            "/api/sign_up",
            data=json.dumps(sign_up_details),
            content_type='application/json'
        )

        self.assertEqual(res.status_code, 400)

    def test_sign_up_with_existing_account(self):
        random_user = UserFactory.create()
        sign_up_details = {
            'username': random_user.username,
            'email': random_user.email,
            'password': Faker().password()
        }

        res = self.app.post(
            "/api/sign_up",
            data=json.dumps(sign_up_details),
            content_type='application/json'
        )

        self.assertEqual(res.status_code, 400)

    def test_sign_in(self):
        user = UserFactory.create(password='aLittle__nice=+=PaTiTo')
        login_details = {
            'username': user.username,
            'password': 'aLittle__nice=+=PaTiTo',
        }

        res = self.app.post(
            "/api/sign_in",
            data=json.dumps(login_details),
            content_type='application/json'
        )

        res_data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(res_data.get('token', None))

    def test_invalid_login(self):
        user = UserFactory.build(password='aLittle__nice=+=PaTiTo')
        login_details = {
            'username': user.username,
            'password': 'aLittle__nice=+=PaTiTo',
        }

        res = self.app.post(
            "/api/sign_in",
            data=json.dumps(login_details),
            content_type='application/json'
        )

        res_data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 401)
        self.assertIsNone(res_data.get('token', None))

    def test_sign_in_with_missing_data(self):
        login_details = {
            'password': 'aLittle__nice=+=PaTiTo',
        }

        res = self.app.post(
            "/api/sign_in",
            data=json.dumps(login_details),
            content_type='application/json'
        )

        self.assertEqual(res.status_code, 400)

    def test_protected_endpoint_unauthorized(self):
        res = self.app.get('/api/whoami', content_type='application/json')

        self.assertEqual(res.status_code, 401)

    def test_protected_endpoint_authorized(self):
        res = self.app.get(
            '/api/whoami',
            content_type='application/json',
            headers=self._authorize())

        self.assertEqual(res.status_code, 200)

    def test_non_existent_route(self):
        fake = Faker()
        url = '/api/{}'.format(fake.md5())

        res = self.app.get(
            url,
            content_type='application/json'
        )

        self.assertEqual(res.status_code, 404)

    def test_json_decode_error(self):
        res = self.app.post(
            '/api/places',
            content_type='application/json',
            headers=self._authorize())

        self.assertEqual(res.status_code, 400)