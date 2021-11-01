from flask import Blueprint
from flask_restful import Api
from .resources import UsersResource, UsersLoginResource

blueprint = Blueprint('users', __name__)
api = Api(blueprint)

api.add_resource(UsersResource, '/api/users', '/api/users/<int:id>', endpoint='users')
api.add_resource(UsersLoginResource, '/api/login', endpoint='user_login')
