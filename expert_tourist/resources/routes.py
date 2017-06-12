import json

from . import AdministrativeResource
from ..models import Route as RouteModel
from ..errors import APIException
from ..schemas import RouteSchema

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
    def get(self):
        pass

    def post(self):
        pass
