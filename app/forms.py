from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, DateField, SelectField, TextAreaField
from wtforms.validators import InputRequired, ValidationError, EqualTo, StopValidation
import re

from app.mysql_service import get_Athlete_by_dorsal

def validate_name(form, email):
    resultado = re.fullmatch('^[a-z]*[.][a-z 0-9]*', email.data)
    if resultado is None:
        email.errors[:] = []
        raise ValidationError('!Email is not valid: name.lastname00')

def validate_dorsal(form, dorsal):
    player = get_Athlete_by_dorsal(dorsal.data)
    if player is not None:
        dorsal.errors[:] = []
        raise ValidationError('!Dorsal is already in use')

def allowed_file(form, image):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'PNG', 'JPG', 'JPEG', 'GIF'])
    split_data = str(image.data).rsplit('.', 1)[1]
    extension = split_data.split("'", 1)[0]
    if not (extension in ALLOWED_EXTENSIONS):
        image.errors[:] = []
        raise ValidationError('!Invalid file extension')  

class login_form(FlaskForm):
    email = StringField('Email', validators=[InputRequired(message='Data required'), validate_name])
    password = PasswordField('Password', validators=[InputRequired(message='Data required')])
    submit = SubmitField('Submit')


class signup_form(FlaskForm):
    choices = [\
        ("1","Goal Keeper"), ("2","Right Fullback"), ("3","Left Fullback"), ("4","Center Back"), ("55","Defending/holding Midfielder"),\
            ("6","Right Midfielder/Winger"), ("7","Central/Box-to-Box Midfielder"), ("8","Striker"), ("9","Attacking Midfielder/Playmaker"),\
                ("10","Left Midfielder/Wingers")]
    id = StringField('Email', validators=[InputRequired(), validate_name])
    password = PasswordField('Pasword', validators=[InputRequired(), EqualTo('confirm', message='!Passwords must match')])
    confirm = PasswordField('Confirm pasword', validators=[InputRequired()])
    name = StringField('Name', validators=[InputRequired()])
    lastname = StringField('Lastname', validators=[InputRequired()])
    height = StringField('Height', validators=[InputRequired()])
    weight = StringField('Wheight', validators=[InputRequired()])
    birthday = DateField('Birthday YYYY-MM-dd', validators=[InputRequired()], format='%Y-%m-%d')
    dorsal = StringField('Dorsal', validators=[InputRequired(), validate_dorsal])
    position = SelectField('Position', choices= choices)
    biography  = TextAreaField('Biography')
    image = FileField('image', validators=[InputRequired()])
    submit = SubmitField()