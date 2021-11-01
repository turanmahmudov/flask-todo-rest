from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate


def identity_loader(user):
    return user.id


migrate = Migrate()

bcrypt = Bcrypt()

db = SQLAlchemy()

jwt = JWTManager()
jwt.user_identity_loader(identity_loader)
