from flask_testing import TestCase

from expert_tourist import create_app
from expert_tourist.models import Tourist, Classifier, TouristClassifier

from ..factories import TouristFactory


class TestTouristClassifier(TestCase):
    def create_app(self):
        app = create_app('config.TestConfig')
        return app

    def setUp(self):
        self.app = self.create_app().test_client()
        self.classifier = TouristClassifier()

    def tearDown(self):
        Tourist.drop_collection()
        Classifier.drop_collection()
        del self.classifier

    def test_classifier_without_previous_data_saved(self):
        TouristFactory.create_batch(20)
        clf = self.classifier.build()  # No previous classifier exists
        self.assertIsNotNone(clf)

        clf = self.classifier.build()  # A previous classifier exists
        self.assertIsNotNone(clf)

    def test_classifier_rebuild(self):
        TouristFactory.create_batch(20)
        clf = self.classifier.build(rebuild=True)

        self.assertIsNotNone(clf)

        TouristFactory.create_batch(20)
        clf = self.classifier.build(rebuild=True)
        self.assertIsNotNone(clf)

    def test_tourist_vector(self):
        tourist = TouristFactory.create()
        vector = self.classifier.vector(tourist)

        self.assertEqual(len(vector), len(self.classifier.Meta.attributes))

    def test_tourist_dataset(self):
        TouristFactory.create_batch(50)

        X, Y = self.classifier.dataset()

        self.assertEqual(len(X), 50)
        self.assertEqual(len(Y), 50)

    def test_tourist_classify(self):
        TouristFactory.create_batch(50)
        tourist = TouristFactory.build()

        class_ = self.classifier.classify(tourist)
        self.assertTrue(class_ in ['c1', 'c2', 'c3', 'c4'])

