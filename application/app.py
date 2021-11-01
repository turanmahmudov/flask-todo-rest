from flask import Flask

from application import tasks, users
from application.settings import ProdConfig
from application.extensions import jwt, db, migrate, bcrypt


def create_app(config_object=ProdConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)

    """Blueprints"""
    app.register_blueprint(users.views.blueprint)
    app.register_blueprint(tasks.views.blueprint)

    """Extensions"""
    jwt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    return app
