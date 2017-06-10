from flask import request
from flask_restful import Resource

from ..errors import APIException
from ..models import Place as PlaceModel
from ..schemas import PlaceSchema

__all__ = ['Place', 'PlaceList']


def _find_place(id: str):
    place = PlaceModel.objects(id=id).first()

    if place is None:
        raise APIException('Place with ID <%s> does not exist', 404)

    return place


class Place(Resource):
    schema = PlaceSchema()

    def get(self, id: str):
        place = _find_place(id)

        return self.schema.dump(place).data

    def put(self, id: str):
        pass

    def delete(self, id: str):
        pass


class PlaceList(Resource):
    schema = PlaceSchema()

    def get(self):
        return self.schema.dump(PlaceModel.objects, many=True).data

    def post(self):
        data = self.schema.loads(request.data)
        if data.errors:
            raise APIException('Invalid request body for type <Place>', errors=data.errors)
        else:
            place = data.data
            place.save()
            return self.schema.dump(place).data, 201
