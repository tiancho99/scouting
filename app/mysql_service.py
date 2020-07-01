from .models import Athlete

def get_Athlete(email):
    athlete = Athlete.query.filter_by(id=email).first()
    return athlete