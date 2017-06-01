from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(config_object=None):
    app_ = Flask(__name__, instance_relative_config=True, static_folder='../react-app/dist',
                 template_folder='../react-app/')

    if config_object:
        app_.config.from_object(config_object)


    from .models import db

    db.init_app(app_)
    bcrypt.init_app(app_)
    jwt.init_app(app_)
    migrate.init_app(app_, db)

    from .views import api as api_bp
    app_.register_blueprint(api_bp, url_prefix='/api')

    return app_


app = create_app('config.DevConfig')


@app.route('/')
def index():
    # Say hello, we're live!
    return render_template('index.html')


@app.route('/<path:path>')
def any_route_to_index(path):
    return render_template('index.html')
