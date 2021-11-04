from application.extensions import bcrypt, db
from flask_jwt_extended import get_jwt_identity
from application.utils.filter_query_builder import filter_query_builder


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255))
    done = db.Column(db.Boolean())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, task, done) -> None:
        db.Model.__init__(self, task=task, done=done)

    @classmethod
    def get_one(cls, task_id):
        current_user_id = get_jwt_identity()
        return Task.query.filter(Task.id == task_id, Task.user_id == current_user_id).first()

    @classmethod
    def get_all(cls, filter_str=None, limit=None, page=None):
        current_user_id = get_jwt_identity()
        query = Task.query
        if filter_str:
            query = filter_query_builder(Task, filter_str)

        query = query.filter(Task.user_id == current_user_id)

        if limit:
            query = query.limit(limit)

        if page:
            query = query.offset((page-1) * limit)

        return query.all()

    def __repr__(self) -> str:
        return f"Todo('{self.task}')"
