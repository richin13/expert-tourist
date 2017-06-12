import mongoengine as me

from . import db


class Route(db.Document):
    places = me.ListField(me.ReferenceField('Place'))
