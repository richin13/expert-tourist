import os
import json

from flask import current_app
from flask_mongoengine import MongoEngine

db = MongoEngine()

__all__ = ['User', 'Place', 'Route', 'Tourist']


class DatasetManager:
    data_source_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../', '../', 'data')
    data_source = None
    filename = ''

    def __init__(self):
        path = os.path.join(self.data_source_path, self.filename)
        if os.path.isfile(path):
            with open(path, 'r') as f:
                self.data_source = json.loads(f.read())

    def load_dataset(self, cls):
        print('Loading data in {}'.format(current_app.config.get('MONGODB_SETTINGS', {'db': 'NONE'})['db']))
        saved_items_count = 0
        if self.data_source:
            for raw_item in self.data_source:
                item = cls(**raw_item)
                item.save()
            saved_items_count = len(self.data_source)
            print('[Done]', end=' ')

        print('Saved a total of {} items from {}'.format(saved_items_count, self.filename))
        return saved_items_count

    def group_by(self, field_name):
        group = {}
        if self.data_source:
            for raw_item in self.data_source:
                value = raw_item.get(field_name, None)
                assert value is not None
                if value not in group:
                    group[value] = 0
                group[value] += 1
        return group


from .classifer import Classifier
from .user import User
from .place import Place, PlaceDatasetManager
from .route import Route
from .tourist import Tourist, TouristDatasetManager, TouristClassifier
