from application.extensions import bcrypt, db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=True)
    token = ""
    tasks = db.relationship("Task", backref="user", lazy=True)

    def __init__(self, username, password=None) -> None:
        super().__init__(self, username=username)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password) -> None:
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value) -> bool:
        return bcrypt.check_password_hash(self.password, value)

    def __repr__(self) -> str:
        return f"User('{self.username}')"
