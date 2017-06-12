import json

from expert_tourist.models import User

from . import TestViewCase
from ..factories import UserFactory


class TestAuthViews(TestViewCase):
    def tearDown(self):
        User.drop_collection()

    def test_sign_up_with_valid_data(self):
        random_user = UserFactory.build()
        sign_up_details = {
            'username': random_user.username,
            'email': random_user.email,
            'password': self.fake.password()
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
            'password': self.fake.password()
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
