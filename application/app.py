from flask import Flask

from application import tasks
from application.settings import ProdConfig

def create_app(config_object=ProdConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)

    """Blueprints"""
    app.register_blueprint(tasks.views.blueprint)

    return app