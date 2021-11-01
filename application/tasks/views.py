from flask import Blueprint
from flask_restful import Api
from .resources import TasksResource, TaskResource

blueprint = Blueprint('tasks', __name__)
api = Api(blueprint)

api.add_resource(TasksResource, '/api/tasks', endpoint='tasks')
api.add_resource(TaskResource, '/api/tasks/<int:task_id>', endpoint='task')
