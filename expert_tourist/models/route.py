import mongoengine as me

from . import db, Place


class Route(db.Document):
    places = me.ListField(me.ReferenceField(Place))
