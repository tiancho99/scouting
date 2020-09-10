from flask import jsonify
from .models import Person, Athlete, Game, GameSchema, Position, record, db
from sqlalchemy import desc, func, asc

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
    athletes = Person.query.filter(Person.id_athlete!=None).all()
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
    records = db.session.query(Person,
        func.sum(record.c.played_time),
        func.sum(record.c.saves),
        func.sum(record.c.clearances),
        func.sum(record.c.centered_passes),
        func.sum(record.c.assists),
        func.sum(record.c.interceptions),
        func.sum(record.c.short_passes),
        func.sum(record.c.long_passes),
        func.sum(record.c.scored_goals),
        func.sum(record.c.scored_penalties),
        func.sum(record.c.scored_freekicks),)\
            .join(Person.athlete).join(record)\
                .order_by(desc(func.sum(record.c.saves)+func.sum(record.c.clearances)+func.sum(record.c.centered_passes)+func.sum(record.c.assists)+func.sum(record.c.interceptions)+func.sum(record.c.short_passes)+func.sum(record.c.long_passes)+func.sum(record.c.scored_goals)+func.sum(record.c.scored_penalties)+func.sum(record.c.scored_freekicks)))\
                    .group_by(record.c.id_athlete)\
                        .all()
    return records

def get_stats_by_position(position):
    print('entraste al metodo')
    print('la posicion es'+position)
    if position=='0':
        return get_stats()
    if position=='1':
        print('portero')
        return get_goal_keeper_stats()
    if position=='2':
        return get_fullback_stats(position)
    if position=='3':
        return get_fullback_stats(position)
    if position=='4':
        return get_fullback_stats(position)
    if position=='5':
        return get_midfielder_stats(position)
    if position=='6':
        return get_midfielder_stats(position)
    if position=='7':
        return get_midfielder_stats(position)
    if position=='8':
        return get_striker_stats(position)
    if position=='9':
        return get_midfielder_stats(position)
    if position=='10':
        return get_midfielder_stats(position)


def get_goal_keeper_stats():
    records = db.session.query(Person,
        func.sum(record.c.played_time),
        func.sum(record.c.saves),
        func.sum(record.c.clearances),
        func.sum(record.c.centered_passes),
        func.sum(record.c.assists),
        func.sum(record.c.interceptions),
        func.sum(record.c.short_passes),
        func.sum(record.c.long_passes),
        func.sum(record.c.scored_goals),
        func.sum(record.c.scored_penalties),
        func.sum(record.c.scored_freekicks),)\
            .join(Person.athlete).join(record)\
                .filter(Athlete.position == '1')\
                    .group_by(record.c.id_athlete)\
                        .order_by(desc(func.sum(record.c.saves) + func.sum(record.c.clearances) + func.sum(record.c.centered_passes)))\
                            .all()
    return records

def get_fullback_stats(position):
    records = db.session.query(Person,
        func.sum(record.c.played_time),
        func.sum(record.c.saves),
        func.sum(record.c.clearances),
        func.sum(record.c.centered_passes),
        func.sum(record.c.assists),
        func.sum(record.c.interceptions),
        func.sum(record.c.short_passes),
        func.sum(record.c.long_passes),
        func.sum(record.c.scored_goals),
        func.sum(record.c.scored_penalties),
        func.sum(record.c.scored_freekicks),)\
            .join(Person.athlete).join(record)\
                .filter(Athlete.position == position)\
                    .group_by(record.c.id_athlete)\
                        .order_by(desc(func.sum(record.c.clearances)+func.sum(record.c.centered_passes)+func.sum(record.c.interceptions)+func.sum(record.c.short_passes)+func.sum(record.c.long_passes)))\
                            .all()
    return records

def get_midfielder_stats(position):
    records = db.session.query(Person,
        func.sum(record.c.played_time),
        func.sum(record.c.saves),
        func.sum(record.c.clearances),
        func.sum(record.c.centered_passes),
        func.sum(record.c.assists),
        func.sum(record.c.interceptions),
        func.sum(record.c.short_passes),
        func.sum(record.c.long_passes),
        func.sum(record.c.scored_goals),
        func.sum(record.c.scored_penalties),
        func.sum(record.c.scored_freekicks),)\
            .join(Person.athlete).join(record)\
                .filter(Athlete.position == position)\
                    .group_by(record.c.id_athlete)\
                        .order_by(desc(func.sum(record.c.centered_passes)+func.sum(record.c.assists)+func.sum(record.c.interceptions)+func.sum(record.c.short_passes)+func.sum(record.c.long_passes)+func.sum(record.c.scored_goals)+func.sum(record.c.scored_penalties)+func.sum(record.c.scored_freekicks)))\
                            .all()
    return records

def get_striker_stats(position):
    records = db.session.query(Person,
        func.sum(record.c.played_time),
        func.sum(record.c.saves),
        func.sum(record.c.clearances),
        func.sum(record.c.centered_passes),
        func.sum(record.c.assists),
        func.sum(record.c.interceptions),
        func.sum(record.c.short_passes),
        func.sum(record.c.long_passes),
        func.sum(record.c.scored_goals),
        func.sum(record.c.scored_penalties),
        func.sum(record.c.scored_freekicks),)\
            .join(Person.athlete).join(record)\
                .filter(Athlete.position == position)\
                    .group_by(record.c.id_athlete)\
                        .order_by(desc(func.sum(record.c.assists)+func.sum(record.c.interceptions)+func.sum(record.c.short_passes)+func.sum(record.c.long_passes)+func.sum(record.c.scored_goals)+func.sum(record.c.scored_penalties)+func.sum(recor+d.c.scored_freekicks)))\
                            .all()
    return records

def get_person_stats(id1, id2):
    records = db.session.query(
        func.sum(record.c.played_time),
        func.sum(record.c.saves),
        func.sum(record.c.clearances),
        func.sum(record.c.centered_passes),
        func.sum(record.c.assists),
        func.sum(record.c.interceptions),
        func.sum(record.c.short_passes),
        func.sum(record.c.long_passes),
        func.sum(record.c.scored_goals),
        func.sum(record.c.scored_penalties),
        func.sum(record.c.scored_freekicks),)\
            .group_by(record.c.id_athlete)\
                .having((record.c.id_athlete == id1) | (record.c.id_athlete == id2))\
                    .all()
    return records    