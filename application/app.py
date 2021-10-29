from flask import Flask

from application import tasks, users
from application.settings import ProdConfig
from application.jwt import jwt

def create_app(config_object=ProdConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)

    """Blueprints"""
    app.register_blueprint(users.views.blueprint)
    app.register_blueprint(tasks.views.blueprint)

    """Extensions"""
    jwt.init_app(app)

    return app
