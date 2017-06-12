from flask import Flask, jsonify
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager

ma = Marshmallow()
cors = CORS()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(config_object=None):
    app = Flask(__name__, instance_relative_config=True)

    if config_object:
        app.config.from_object(config_object)

    from .models import db

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    api = Api(app, prefix='/api')
    register_api_resources(api)

    from .views import api as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    register_error_handlers(app)

    return app


def register_api_resources(api):
    from .resources.places import Place, PlaceList
    from .resources.routes import Route, RouteList

    api.add_resource(Place, '/places/<string:id>', endpoint='api.place')
    api.add_resource(PlaceList, '/places')
    api.add_resource(Route, '/routes/<string:id>', endpoint='api.route')
    api.add_resource(RouteList, '/routes', '/recommend')


def register_error_handlers(app):
    from .errors import APIException
    import json.decoder as jd

    @app.errorhandler(APIException)
    def handle_api_exception(error: APIException):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(404)
    def handle_not_found(error):
        return handle_api_exception(APIException(
            'The requested URL was not found on the server.  '
            'If you entered the URL manually please check your spelling and try again.', status_code=404))

    @app.errorhandler(jd.JSONDecodeError)
    def handle_json_parse_error(error):
        return handle_api_exception(APIException(
            'The browser (or proxy) sent a request that this server could not understand.'))
