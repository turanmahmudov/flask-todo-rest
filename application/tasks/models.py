from application.extensions import bcrypt, db


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255))
    done = db.Column(db.Boolean())

    def __init__(self, task, done) -> None:
        db.Model.__init__(self, task=task, done=done)

    def __repr__(self) -> str:
        return f"Todo('{self.task}')"
