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

    from .errors import APIException

    @app.errorhandler(APIException)
    def handle_api_exception(error: APIException):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    return app


def register_api_resources(api):
    from .resources.places import Place, PlaceList

    api.add_resource(Place, '/places/<string:id>', endpoint='api.place')
    api.add_resource(PlaceList, '/places')

