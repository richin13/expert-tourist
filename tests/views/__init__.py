from faker import Faker
from flask_testing import TestCase

from expert_tourist import create_app

from ..factories import UserFactory


class TestViewCase(TestCase):
    fake = Faker()

    def create_app(self):
        return create_app('config.TestConfig')

    def setUp(self):
        self.app = self.create_app().test_client()

    def _authorize(self):
        user = UserFactory.create()
        return {'Authorization': user.token}
