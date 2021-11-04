from flask_restful import Resource, reqparse, fields, marshal_with, abort
from flask_jwt_extended import create_access_token
from .models import User

parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)

task_fields = {
    'id': fields.Integer,
    'task': fields.String,
    'done': fields.Boolean
}

resource_fields = {
    'username': fields.String,
    'token': fields.String
}


class UsersResource(Resource):
    def get(self):
        pass


class UsersLoginResource(Resource):
    @marshal_with(resource_fields, envelope='user')
    def post(self):
        data = parser.parse_args()

        user = User.query.filter_by(username=data['username']).first()
        if user is not None and user.check_password(data['password']):
            user.token = create_access_token(identity=user, fresh=True)

            return user
        else:
            abort(401, message="User not found")
