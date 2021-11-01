from flask_restful import Resource, reqparse, fields, marshal_with, abort
from flask_jwt_extended import jwt_required
from .models import Task
from application.extensions import db

parser = reqparse.RequestParser()
parser.add_argument('task', help='This field cannot be blank', required=True)
parser.add_argument('done', type=bool, required=False, default=False)

resource_fields = {
    'id': fields.Integer,
    'task': fields.String,
    'done': fields.Boolean
}


class TasksResource(Resource):
    @jwt_required()
    @marshal_with(resource_fields, envelope='tasks')
    def get(self):
        tasks = Task.query.all()
        return tasks

    @jwt_required()
    @marshal_with(resource_fields, envelope='task')
    def post(self):
        data = parser.parse_args()

        task = Task(data['task'], data['done'])
        try:
            db.session.add(task)
            db.session.commit()
        except:
            abort(400)

        return task, 201


class TaskResource(Resource):
    @jwt_required()
    @marshal_with(resource_fields, envelope='task')
    def get(self, task_id=None):
        task = Task.query.get(task_id)

        if not task:
            abort(404, message="Task not found")

        return task

    @jwt_required()
    @marshal_with(resource_fields, envelope='task')
    def put(self, task_id=None):
        if not task_id:
            abort(404, message="Task not found")

        task = Task.query.get(task_id)

        if not task:
            abort(404, message="Task not found")

        data = parser.parse_args()

        try:
            task.task = data['task']
            task.done = data['done']
            db.session.commit()
        except:
            abort(400)

        return task, 201

    @jwt_required()
    def delete(self, task_id=None):
        if not task_id:
            abort(404, message="Task not found")

        task = Task.query.get(task_id)

        if not task:
            abort(404, message="Task not found")

        db.session.delete(task)
        db.session.commit()

        return {}
