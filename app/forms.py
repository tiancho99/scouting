from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, DateField, SelectField, TextAreaField, HiddenField, IntegerField, FormField
from wtforms.validators import InputRequired, ValidationError, EqualTo, StopValidation
import re

from app.mysql_service import get_Athlete_by_dorsal, get_Person, get_People

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

def avalidate_dorsal(form, dorsal):
    player = get_Athlete_by_dorsal(dorsal.data)

    if player is not None and dorsal.data != str(player.dorsal):
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
        ("1","Goal Keeper"), ("2","Right Fullback"), ("3","Left Fullback"), ("4","Center Back"), ("5","Defending/holding Midfielder"),\
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

class logout_form(FlaskForm):
    logout = SubmitField()

class search_person_form(FlaskForm):
    people = get_People()
    person_list =[]
    for person in people:
        if person.athlete != None:
            person_list.append(('{}'.format(person.id),'{} {}'.format(person.lastname, person.name)))
    player = SelectField('Select player', choices=person_list)
    search = SubmitField()

class delete_person_form(FlaskForm):
    people = get_People()
    person_list =[]
    for person in people:
        if person.athlete != None:
            person_list.append(('{}'.format(person.id),'{} {}'.format(person.lastname, person.name)))
    player = SelectField('Select player', choices=person_list)
    search = SubmitField('Delete')

def create_edit_form(id):
    class edit_form(FlaskForm):
        pass
    player = get_Person(id)
    choices = [\
        ("1","Goal Keeper"), ("2","Right Fullback"), ("3","Left Fullback"), ("4","Center Back"), ("5","Defending/holding Midfielder"),\
            ("6","Right Midfielder/Winger"), ("7","Central/Box-to-Box Midfielder"), ("8","Striker"), ("9","Attacking Midfielder/Playmaker"),\
                ("10","Left Midfielder/Wingers")]
    
    id = HiddenField('id', default=player.id, validators=[InputRequired()])
    email = StringField('Email', validators=[validate_name, InputRequired()], default=player.id)
    name = StringField('Name',default=player.name, validators=[InputRequired()])
    lastname = StringField('Lastname',default=player.lastname, validators=[InputRequired()])
    birthday = DateField('Birthday YYYY-MM-dd', format='%Y-%m-%d',default=player.birthday, validators=[InputRequired()])
    height = StringField('Height',default=player.athlete.height, validators=[InputRequired()])
    weight = StringField('Wheight',default=player.athlete.weight, validators=[InputRequired()])
    dorsal = StringField('Dorsal', validators=[validate_dorsal, InputRequired()],default=player.athlete.dorsal)
    position = SelectField('Position', choices= choices,default=player.athlete.position, validators=[InputRequired()])
    submit = SubmitField()
    setattr(edit_form, 'id', id) 
    setattr(edit_form, 'email', email)
    setattr(edit_form, 'name', name)
    setattr(edit_form, 'lastname', lastname)
    setattr(edit_form, 'birthday', birthday)
    setattr(edit_form, 'height', height)
    setattr(edit_form, 'weight', weight)
    setattr(edit_form, 'dorsal', dorsal)
    setattr(edit_form, 'position', position)
    setattr(edit_form, 'submit', submit)
    
    return edit_form()

class edit_form(FlaskForm):
    choices = [\
    ("1","Goal Keeper"), ("2","Right Fullback"), ("3","Left Fullback"), ("4","Center Back"), ("5","Defending/holding Midfielder"),\
        ("6","Right Midfielder/Winger"), ("7","Central/Box-to-Box Midfielder"), ("8","Striker"), ("9","Attacking Midfielder/Playmaker"),\
            ("10","Left Midfielder/Wingers")]

    id = HiddenField('id')
    email = StringField('Email', validators=[validate_name])
    name = StringField('Name')
    lastname = StringField('Lastname')
    birthday = DateField('Birthday YYYY-MM-dd', format='%Y-%m-%d')
    height = StringField('Height')
    weight = StringField('Wheight')
    dorsal = StringField('Dorsal', validators=[avalidate_dorsal])
    position = SelectField('Position', choices= choices)
    submit = SubmitField()

class assess_form(FlaskForm):
    player = FormField(search_person_form)
    played_time = IntegerField('Minutos jugados',default=0)
    saves = IntegerField('Atajadas',default=0)
    clearances = IntegerField('Despejes',default=0)
    centered_passes = IntegerField('Centros',default=0)
    assists = IntegerField('Asistencias',default=0)
    interceptions = IntegerField('Intercepciones',default=0)
    short_passes = IntegerField('Pases cortos',default=0)
    long_passes = IntegerField('Pases largos',default=0)
    scored_goals = IntegerField('Goles de campo',default=0)
    scored_penalties = IntegerField('Goles de penal',default=0)
    scored_freekicks = IntegerField('Goles de tiro libre',default=0)
    submit = SubmitField('Enviar')
    