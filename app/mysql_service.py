from flask import jsonify
from .models import Person, Athlete, Game, GameSchema, Position, Record, db
from sqlalchemy import desc, func

def get_Person(email):
    person = Person.query.filter_by(id=email).first()
    return person

def get_People():
    people = Person.query.order_by(Person.lastname).all()
    return people

def get_Athlete_by_dorsal(dorsal):
    athlete = Athlete.query.filter_by(dorsal=dorsal).first()
    return athlete

def get_Athletes():
    athletes = Person.query.all()
    return athletes

def get_Games():
    games_schema = GameSchema(many=True)
    games = Game.query.all()
    result = games_schema.dump(games)

    return jsonify(result)

def get_games():
    games = Game.query.order_by(desc(Game.id)).all()
    return games

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

def get_positions():
    positions = Position.query.all()
    return positions

def get_stats():
    # goals = db.session.query(func.sum(Record.played_time),
    #                             func.sum(Record.saves),
    #                             func.sum(Record.clearances),
    #                             func.sum(Record.centered_passes),
    #                             func.sum(Record.assists),
    #                             func.sum(Record.interceptions),
    #                             func.sum(Record.short_passes),
    #                             func.sum(Record.long_passes),
    #                             func.sum(Record.scored_goals),
    #                             func.sum(Record.scored_penalties),
    #                             func.sum(Record.scored_freekicks),
    #                             Record.id_athlete).group_by(Record.id_athlete).order_by(desc(func.sum(Record.played_time))).all()
    #                             # Record.id_athlete).group_by(Record.id_athlete).order_by(desc(func.sum(Record.saves+Record.centered_passes))).all()
    # return
    return db.session.query(Person, Athlete, Record).filter(Person.id_athlete==Athlete.id).filter(Athlete.id == Record.id_athlete).all()
def get_athlete_stats():
    pass