import mongoengine as me

from . import db, Place
from ..utils import CLASSES_ENCODING

class Route(db.Document):
    places = me.ListField(me.ReferenceField(Place))
    start_latitude = me.FloatField()
    start_longitude = me.FloatField()
    tourist_type = me.IntField(required=True, choices=CLASSES_ENCODING)
