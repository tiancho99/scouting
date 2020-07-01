from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Athlete(UserMixin, db.Model):
    __tablename__ = 'athlete'
    id = db.Column('user', db.String(40), primary_key=True)

    password = db.Column('password', db.String(200), nullable=False)

    name = db.Column('name', db.String(100), nullable=False)

    lastname = db.Column('lastname', db.String(100), nullable=False)

    height = db.Column('height', db.Float, nullable=False)

    weight = db.Column('weight', db.Float, nullable=False)

    birthday = db.Column('birthday', db.Date, nullable=False)

    dorsal = db.Column('dorsal', db.Integer, nullable=False)


    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)