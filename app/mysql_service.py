from flask import jsonify
from .models import Person, Athlete, Game, GameSchema, db

def get_Person(email):
    person = Person.query.filter_by(id=email).first()
    return person

def get_People():
    people = Person.query.order_by(Person.lastname).all()
    return people

def get_Athlete_by_dorsal(dorsal):
    athlete = Athlete.query.filter_by(dorsal=dorsal).first()
    return athlete


def get_Games():
    games_schema = GameSchema(many=True)
    games = Game.query.all()
    result = games_schema.dump(games)

    return jsonify(result)

def put_Game(datetime, location, training):
    game = Game(datetime, location, training)
    db.session.add(game)
    db.session.commit()


def put_Athlete(id, password, name, lastname, birthday, biography, image, height, weight, dorsal, position):
    athlete = Athlete(height, weight, dorsal, position)
    db.session.add(athlete)
    db.session.commit()
    __put_person(athlete, id, password, name, lastname, birthday, biography, image)


def __put_person(athlete, id, password, name, lastname, birthday, biography, image):
    person = Person(id, name, lastname, birthday, biography, image)
    person.set_athlete(athlete)
    person.set_password(password)
    db.session.add(person)
    db.session.commit()

def update_Athlete(id, email, name, lastname, birthday, height, weight, dorsal, position):
    person = Person.query.filter_by(id=id).first()
    print(email)
    person.id = email
    person.name = name
    person.lastname = lastname
    person.birthday = birthday
    person.athlete.height = height
    person.athlete.weight = weight
    person.athlete.dorsal = dorsal
    person.athlete.position = position
    db.session.commit()

def delete_Person(person):
    db.session.delete(person)
    db.session.commit()