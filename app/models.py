from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Athlete(UserMixin, db.Model):
    __tablename__ = 'athlete'

    def __init__(self, id, name, lastname, height, weight, birthday, dorsal, position, is_coach, image):
        self.id = id
        self.name = name
        self.lastname = lastname
        self.height = height
        self.weight = weight
        self.birthday = birthday
        self.dorsal = dorsal
        self.image = image
        self.position = position
        self.is_coach = is_coach


    id = db.Column('id', db.String(40), primary_key=True)

    password = db.Column('password', db.String(200), nullable=False)

    name = db.Column('name', db.String(100), nullable=False)

    lastname = db.Column('lastname', db.String(100), nullable=False)

    height = db.Column('height', db.Float(), nullable=False)

    weight = db.Column('weight', db.Float(), nullable=False)

    birthday = db.Column('birthday', db.Date(), nullable=False)

    dorsal = db.Column('dorsal', db.Integer(), nullable=False)

    position = db.Column('position', db.Integer(), nullable=False)

    is_coach = db.Column('is_coach', db.Boolean(), nullable=False)

    image = db.Column('image', db.String(), nullable=True)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        print(password)
        print(self.password)
        return check_password_hash(self.password, password)