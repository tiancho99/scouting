from .models import Athlete, db

def get_Athlete(email):
    athlete = Athlete.query.filter_by(id=email).first()
    return athlete

def get_Athlete_by_dorsal(dorsal):
    athlete = Athlete.query.filter_by(dorsal=dorsal).first()
    return athlete

def put_Athlete(id, password, name, lastname, height, weight, birthday, dorsal, posicion, image):
    athlete = Athlete(id, name, lastname, height, weight, birthday, dorsal, posicion, False, image)
    athlete.set_password(password)
    db.session.add(athlete)
    db.session.commit()