from .models import Person, Athlete, db

def get_Person(email):
    person = Person.query.filter_by(id=email).first()
    return person

def get_Athlete_by_dorsal(dorsal):
    athlete = Athlete.query.filter_by(dorsal=dorsal).first()
    return athlete


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