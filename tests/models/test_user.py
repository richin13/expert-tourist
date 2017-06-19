import json
from faker import Faker
from flask_testing import TestCase

from expert_tourist import create_app
from expert_tourist.models import User, Place

from ..factories import UserFactory


class TestPlaceModel(TestCase):
    def create_app(self):
        app = create_app('config.TestConfig')
        return app

    def setUp(self):
        self.app = self.create_app().test_client()

    def tearDown(self):
        Place.drop_collection()
        User.drop_collection()

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
