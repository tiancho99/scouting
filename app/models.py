from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_marshmallow import Marshmallow
from time import strftime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
ma = Marshmallow()
conn = create_engine('mysql://sebastian:supertiancho99@localhost/scouting', convert_unicode=True)

#! person
class Person(UserMixin, db.Model):
    __tablename__ = 'person'

    def __init__(self, id, name, lastname, birthday, biography, image):
        self.id = id
        self.name = name
        self.lastname = lastname
        self.birthday = birthday
        self.biography = biography
        self.image = image

    id = db.Column('id', db.String(40), primary_key=True)

    password = db.Column('password', db.String(200), nullable=False)

    name = db.Column('name', db.String(100), nullable=False)

    lastname = db.Column('lastname', db.String(100), nullable=False)

    birthday = db.Column('birthday', db.Date(), nullable=False)

    biography = db.Column('biography', db.Date(), nullable=True)

    image = db.Column('image', db.String(500), nullable=True)

    id_athlete = db.Column(db.Integer, db.ForeignKey('athlete.id'))

    id_coach = db.Column(db.Integer, db.ForeignKey('coach.id'))

    def set_athlete(self, athlete):
        self.athlete = athlete
        self.coach = None

    def set_coach(self, coach):
        self.coach = coach
        self.athlete = None

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):

        return check_password_hash(self.password, password)

#! Record
record = db.Table('record',
    db.Column('id_game', db.String(100), db.ForeignKey('game.id'), primary_key=True),
    db.Column('id_athlete', db.Integer, db.ForeignKey('athlete.id'), primary_key=True),
    db.Column('played_time', db.Integer, nullable=False),
    db.Column('saves', db.Integer, nullable=True),
    db.Column('clearances', db.Integer, nullable=True),
    db.Column('centered_passes', db.Integer, nullable=True),
    db.Column('assists', db.Integer, nullable=True),
    db.Column('interceptions', db.Integer, nullable=True),
    db.Column('short_passes', db.Integer, nullable=True),
    db.Column('long_passes', db.Integer, nullable=True),
    db.Column('scored_goals', db.Integer, nullable=True),
    db.Column('scored_penalties', db.Integer, nullable=True),
    db.Column('scored_freekicks', db.Integer, nullable=True)
)


#! Atlete
class Athlete(db.Model):
    __tablename__ = 'athlete'

    def __init__(self, height, weight ,dorsal, position):
        self.id = None
        self.height = height
        self.weight = weight
        self.dorsal = dorsal
        self.position = position

    
    id = db.Column('id', db.Integer, primary_key=True)

    height = db.Column('height', db.Float, nullable=False)

    weight = db.Column('weight', db.Float, nullable=False)
    
    dorsal = db.Column('dorsal', db.Integer, nullable=False)

    position = db.Column('position', db.ForeignKey('position.id'))

    person = db.relationship('Person', backref='athlete', lazy=False, uselist=False)

    record = db.relationship('Game', secondary=record, lazy='subquery', backref=db.backref('athlete', lazy=False))



#!position
class Position(db.Model):
    __tablename__= 'position'
    id = db.Column('id', db.Integer, primary_key=True)

    description = db.Column('description', db.String(50), nullable=False)

    athlete = db.relationship('Athlete', backref='pos', lazy=False, uselist=False)


#!Coach
class Coach(db.Model):
    __tablename__ = 'coach'

    def __init__(self, especialization, link):
        self.id = None
        self.especialization = especialization
        self.link = link
    
    id = db.Column('id', db.Integer, primary_key=True)

    especialization = db.Column('especialization', db.String(100), nullable=False)

    link = db.Column('link', db.String(500), nullable=True)

    person = db.relationship('Person', backref='coach', lazy=False, uselist=False)

#!Game
class Game(db.Model):
    __tablename__= 'game'

    def __init__(self, id, location, training):
        self.id = id
        self.location = location
        self.training = training

    id = db.Column('id', db.String(12), primary_key=True)

    location = db.Column('location', db.String(100), nullable=False)

    training = db.Column('training', db.Boolean, nullable=False)
    

#! Game Schema
class GameSchema(ma.Schema):
    class Meta:
        fields = ('id', 'location', 'training')

