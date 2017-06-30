import json
from flask import request, jsonify

from . import AdministrativeResource
from ..models import Route as RouteModel, Place, TouristClassifier
from ..errors import APIException
from ..schemas import RouteSchema, TouristSchema
from ..builder import RouteBuilder

__all__ = ['Route', 'RouteList']


def _find_route(id: str):
    route = RouteModel.objects(id=id).first()

    if route is None:
        raise APIException('Route with ID <{}> does not exist.'.format(id), status_code=404)

    return route


class Route(AdministrativeResource):
    schema = RouteSchema()

    def get(self, id: str):
        route = _find_route(id)

        return self.schema.dump(route).data

    def put(self, id: str):
        super(Route, self).put(id)
        raise APIException('This feature is not implemented.', status_code=501)

    def delete(self, id: str):
        super(Route, self).delete(id)
        raise APIException('This feature is not implemented.', status_code=501)


class RouteList(AdministrativeResource):
    schema = TouristSchema()
    route_schema = RouteSchema()

    def get(self):
        paginate = bool(request.args.get('paginate', False))
        routes = RouteModel.objects
        if paginate:
            page = int(request.args.get('page', 1))
            routes = routes.paginate(page=page, per_page=15).items
            return jsonify(page=page, result=self.route_schema.dump(routes, many=True).data)

        return self.route_schema.dump(routes, many=True).data

    def post(self):
        result = self.schema.loads(request.data.decode('utf-8'))
        if result.errors:
            raise APIException('Invalid request body for type <Tourist>', errors=result.errors)

        # Step 1: Classify the tourists
        tourist = result.data
        classifier = TouristClassifier()
        tourist.tourist_type = classifier.classify(tourist)
        tourist.save()

        # Step 2: Fetch all the places suitable for that tourist
        places = Place.find_for(tourist)

        # Step 3: Pass the tourist and the places to the routes builder.
        routes = RouteBuilder(tourist).build_routes(places)

        return self.route_schema.dump(routes, many=True).data
