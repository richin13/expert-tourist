import json
import mongoengine as me
from datetime import datetime

from . import db, DatasetManager, Classifier
from ..utils import AREA_ENCODING, BUDGET_ENCODING, TRAVEL_DIST_ENCODING, ACTIVITIES_ENCODING, CLASSES_ENCODING


class Tourist(db.Document):
    """
    Model to represent the user (tourist) that is requesting a new recommendation
    
    :parameter: vehicle The type of vehicle that the user has. It can be a vehicle that can be easily used to access
                    hard-to-reach areas. This can be used to decide whether to recommend touristic places that are
                    known to be hard-to-reach areas (Mountains for example)
                    
    :parameter: budget The budget of the tourist, can be low, moderate or high and depending upon this value we can de-
                        cide whether to recommend expensive places or not.
                        
    :parameter: travel_dist How far the user is willing to travel. Long distances will require the route to include
                            hosting options if the user has a high budget. 
    """
    area = me.IntField(required=True, choices=AREA_ENCODING)
    budget = me.IntField(required=True, choices=BUDGET_ENCODING)
    travel_dist = me.IntField(required=True, choices=TRAVEL_DIST_ENCODING)
    activity = me.IntField(required=True, choices=ACTIVITIES_ENCODING)
    tourist_type = me.IntField(choices=CLASSES_ENCODING)
    coordinates = me.PointField()
    created_at = me.DateTimeField(default=datetime.now())

    class Encoder(json.encoder.JSONEncoder):
        def encode(self, o):
            if type(o) == Tourist:
                o = {
                    'area': o.area,
                    'budget': o.budget,
                    'travel_dist': o.travel_dist,
                    'activity': o.activity,
                    'tourist_type': o.tourist_type,
                    'coordinates': o.coordinates,
                    'created_at': o.created_at.isoformat(),
                }

            return super(Tourist.Encoder, self).encode(o)



class TouristClassifier(Classifier):
    class Meta:
        model = Tourist
        attributes = ['area', 'budget', 'travel_dist', 'activity']
        class_attribute = 'tourist_type'


class TouristDatasetManager(DatasetManager):
    filename = 'tourists.json'
