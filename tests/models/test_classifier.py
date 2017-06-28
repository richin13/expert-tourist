from flask_testing import TestCase

from expert_tourist import create_app
from expert_tourist.models import Tourist, Classifier, TouristClassifier, TouristDatasetManager

from ..factories import TouristFactory


class TestTouristClassifier(TestCase):
    def create_app(self):
        app = create_app('config.TestConfig')
        return app

    def setUp(self):
        self.app = self.create_app().test_client()
        self.classifier = TouristClassifier()
        TouristDatasetManager().load_dataset(Tourist)

    def tearDown(self):
        Tourist.drop_collection()
        Classifier.drop_collection()
        del self.classifier

    def test_classifier_without_previous_data_saved(self):
        clf = self.classifier.build()  # No previous classifier exists
        self.assertIsNotNone(clf)

        clf = self.classifier.build()  # A previous classifier exists
        self.assertIsNotNone(clf)

    def test_classifier_rebuild(self):
        clf = self.classifier.build(rebuild=True)

        self.assertIsNotNone(clf)

        clf = self.classifier.build(rebuild=True)
        self.assertIsNotNone(clf)

    def test_tourist_vector(self):
        tourist = TouristFactory.create()
        vector = self.classifier.vector(tourist)

        self.assertEqual(len(vector), len(self.classifier.Meta.attributes))

    def test_tourist_dataset(self):
        X, Y = self.classifier.dataset()

        self.assertEqual(len(X), 20)
        self.assertEqual(len(Y), 20)

    def test_tourist_classify(self):
        tourist = TouristFactory.build()

        class_ = self.classifier.classify(tourist)
        self.assertTrue(class_ in [0, 1, 2])

    def test_tourist_classify_correct_class(self):
        import random
        tourist_type = random.choice([0, 1, 2])
        t = Tourist.objects(tourist_type=tourist_type).first()

        class_ = self.classifier.classify(t)
        self.assertEqual(class_, t.tourist_type)
