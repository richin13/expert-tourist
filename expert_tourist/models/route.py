import json
import mongoengine as me

from . import db, Place
from ..utils import CLASSES_ENCODING


class Route(db.Document):
    places = me.ListField(me.ReferenceField(Place))
    coordinates = me.PointField(required=True)
    tourist_type = me.IntField(required=True, choices=CLASSES_ENCODING)

    @staticmethod
    def from_path(path, tourist):
        route = Route(places=path, coordinates=tourist.coordinates, tourist_type=tourist.tourist_type)
        route.save()
        return route
