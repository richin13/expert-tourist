import mongoengine as me

from . import db
from ..utils import VEHICLE_ENCODINGS, BUDGET_ENCODING, TRAVEL_DIST_ENCODING, ACTIVITIES_ENCODING


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
    vehicle = me.IntField(required=True, choices=VEHICLE_ENCODINGS)
    budget = me.IntField(required=True, choices=BUDGET_ENCODING)
    travel_dist = me.IntField(required=True, choices=TRAVEL_DIST_ENCODING)
    activity = me.IntField(required=True, choices=ACTIVITIES_ENCODING)
    tourist_type = me.StringField(required=True, max_length=32)
    latitude = me.FloatField(required=True)
    longitude = me.FloatField(required=True)
