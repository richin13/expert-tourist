from expert_tourist.models import User

from flask_testing import TestCase
from expert_tourist import app
from expert_tourist.models import db
import json


class BaseTestConfig(TestCase):
    default_user = {
        "email": "default@gmail.com",
        "password": "something2"
    }

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        self.app = self.create_app().test_client()
        db.create_all()
        # res = self.app.post(
        #     "/api/create_user",
        #     data=json.dumps(self.default_user),
        #     content_type='application/json'
        # )
        #
        # self.token = json.loads(res.data.decode("utf-8"))["token"]

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestAPI(BaseTestConfig):
    random_user = {
        'email': 'shameless-driver2022@live.cr',
        'password': 'tmslaegolbin//tm'
    }

    def test_sign_up(self):
        self.assertIsNone(User.query.filter_by(email=self.random_user['email']).first())

        res = self.app.post(
            "/api/sign_up",
            data=json.dumps(self.random_user),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)
        self.assertTrue(json.loads(res.data.decode("utf-8"))["token"])
        self.assertEqual(
            User.query.filter_by(email=self.random_user["email"]).first().email,
            self.random_user["email"]
        )

    def test_user_validate_credentials(self):
        user = User(**self.random_user).create()
        self.assertIsNotNone(user)
        self.assertIsNotNone(self.random_user['email'], self.random_user['password'])

