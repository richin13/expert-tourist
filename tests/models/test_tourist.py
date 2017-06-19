from flask_testing import TestCase

from expert_tourist import create_app
from expert_tourist.models import Tourist, TouristDatasetManager


class TestModels(TestCase):
    def create_app(self):
        app = create_app('config.TestConfig')
        return app

    def setUp(self):
        self.app = self.create_app().test_client()

    def tearDown(self):
        Tourist.drop_collection()

    def test_tourist_loader(self):
        loader = TouristDatasetManager()
        saved = loader.load_dataset(Tourist)

        self.assertTrue(saved >= Tourist.objects.count())
