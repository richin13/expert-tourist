from flask_mongoengine import MongoEngine

db = MongoEngine()

from .user import User
from .place import Place, PlaceDatasetManager
from .route import Route
