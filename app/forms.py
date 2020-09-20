from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, DateField, SelectField, TextAreaField, HiddenField, IntegerField, FormField
from wtforms.validators import InputRequired, ValidationError, EqualTo, StopValidation
import re

from app.mysql_service import get_Athlete_by_dorsal, get_Person, get_People, get_games, get_positions

def validate_name(form, email):
    resultado = re.fullmatch('^[a-z]*[.][a-z 0-9]*', email.data)
    if resultado is None:
        email.errors[:] = []
        raise ValidationError('!El correo ingresado no es valido: nombre.apellido00')

def validate_dorsal(form, dorsal):
    player = get_Athlete_by_dorsal(dorsal.data)
    if player is not None:
        dorsal.errors[:] = []
        raise ValidationError('!El dorsal elegido ya está en uso')

def avalidate_dorsal(form, dorsal):
    player = get_Athlete_by_dorsal(dorsal.data)

    if player is not None and dorsal.data != str(player.dorsal):
        dorsal.errors[:] = []
        raise ValidationError('!El dorsal elegido ya está en uso')

def allowed_file(form, image):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'PNG', 'JPG', 'JPEG', 'GIF'])
    split_data = str(image.data).rsplit('.', 1)[1]
    extension = split_data.split("'", 1)[0]
    if not (extension in ALLOWED_EXTENSIONS):
        image.errors[:] = []
        raise ValidationError('!Invalid file extension')  

class login_form(FlaskForm):
    email = StringField('Correo', validators=[InputRequired(message='Campo requerido'), validate_name])
    password = PasswordField('Contraseña', validators=[InputRequired(message='campo requeridp')])
    submit = SubmitField('Enviar')


class signup_form(FlaskForm):
    choices = [\
        ("1","Arquero"), ("2","Defensa derecho"), ("3","Defensa izquierdo"), ("4","Defensa central"), ("5","Defensa/Mediocampista de contencion"),\
            ("6","Mediocampista derecho/exterior"), ("7","Central/ Mediocampista"), ("8","Delantero"), ("9","Mediocampista ataque/armador"),\
                ("10","Mediocampista izquierdo/exterior")]

    id = StringField('Correo', validators=[InputRequired(), validate_name])
    password = PasswordField('Contraseña', validators=[InputRequired(), EqualTo('confirm', message='!Passwords must match')])
    confirm = PasswordField('Confirmar contraseña', validators=[InputRequired()])
    name = StringField('Nombre', validators=[InputRequired()])
    lastname = StringField('Apellidos', validators=[InputRequired()])
    height = StringField('Estatura', validators=[InputRequired()])
    weight = StringField('Peso', validators=[InputRequired()])
    birthday = DateField('Cumpleaños', validators=[InputRequired()], format='%Y-%m-%d')
    dorsal = StringField('Dorsal', validators=[InputRequired(), validate_dorsal])
    position = SelectField('Posicion', choices= choices)
    biography  = TextAreaField('Biografia')
    image = FileField('Foto', validators=[InputRequired()])
    submit = SubmitField()

class logout_form(FlaskForm):
    logout = SubmitField()

class search_person_form(FlaskForm):
    people = get_People()
    person_list =[]
    for person in people:
        if person.athlete != None:
            person_list.append(('{}'.format(person.id),'{} {}'.format(person.lastname, person.name)))
    player = SelectField('Seleccionar jugador', choices=person_list)
    search = SubmitField()

class delete_person_form(FlaskForm):
    people = get_People()
    person_list =[]
    for person in people:
        if person.athlete != None:
            person_list.append(('{}'.format(person.id),'{} {}'.format(person.lastname, person.name)))
    player = SelectField('Seleccionar jugador', choices=person_list)
    search = SubmitField('Borrar')

def create_edit_form(id):
    class edit_form(FlaskForm):
        pass
    player = get_Person(id)
    choices = [\
        ("1","Arquero"), ("2","Defensa derecho"), ("3","Defensa izquierdo"), ("4","Defensa central"), ("5","Defensa/Mediocampista de contencion"),\
            ("6","Mediocampista derecho/exterior"), ("7","Central/ Mediocampista"), ("8","Delantero"), ("9","Mediocampista ataque/armador"),\
                ("10","Mediocampista izquierdo/exterior")]
    
    id = HiddenField('id', default=player.id, validators=[InputRequired()])
    email = StringField('Correo', validators=[validate_name, InputRequired()], default=player.id)
    name = StringField('Nombre',default=player.name, validators=[InputRequired()])
    lastname = StringField('apellidos',default=player.lastname, validators=[InputRequired()])
    birthday = DateField('Cumpleaños', format='%Y-%m-%d',default=player.birthday, validators=[InputRequired()])
    height = StringField('Estatura',default=player.athlete.height, validators=[InputRequired()])
    weight = StringField('Peso',default=player.athlete.weight, validators=[InputRequired()])
    dorsal = StringField('Dorsal', validators=[validate_dorsal, InputRequired()],default=player.athlete.dorsal)
    position = SelectField('Posicion', choices= choices,default=player.athlete.position, validators=[InputRequired()])
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
        ("1","Arquero"), ("2","Defensa derecho"), ("3","Defensa izquierdo"), ("4","Defensa central"), ("5","Defensa/Mediocampista de contencion"),\
            ("6","Mediocampista derecho/exterior"), ("7","Central/ Mediocampista"), ("8","Delantero"), ("9","Mediocampista ataque/armador"),\
                ("10","Mediocampista izquierdo/exterior")]

    id = HiddenField('id')
    email = StringField('Correo', validators=[validate_name])
    name = StringField('Nombre')
    lastname = StringField('Apellido')
    birthday = DateField('Cumpleaños', format='%Y-%m-%d')
    height = StringField('Estatura')
    weight = StringField('Peso')
    dorsal = StringField('Dorsal', validators=[avalidate_dorsal])
    position = SelectField('Posicion', choices= choices)
    submit = SubmitField()

class assess_form(FlaskForm):
    games = get_games()
    gameList = []
    for game in games:
        choice = ('{}'.format(game.id), '{}'.format(game.id))
        gameList.append(choice)

    player = FormField(search_person_form)
    matches = SelectField('Partido', choices=gameList)
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

class select_position_form(FlaskForm):
    choices = [\
        ("1","Arquero"), ("2","Defensa derecho"), ("3","Defensa izquierdo"), ("4","Defensa central"), ("5","Defensa/Mediocampista de contencion"),\
            ("6","Mediocampista derecho/exterior"), ("7","Central/ Mediocampista"), ("8","Delantero"), ("9","Mediocampista ataque/armador"),\
                ("10","Mediocampista izquierdo/exterior")]
    
    position = SelectField('Agrupar por:', choices=choices, validators=[InputRequired()])
    submit = SubmitField('Enviar')


class get_versus_form(FlaskForm):
    people = get_People()
    person_list =[]
    for person in people:
        if person.athlete != None:
            person_list.append((str(person.athlete.id),'{} {}'.format(person.lastname, person.name)))
    select1 = SelectField('Selecciona el jugador 1', choices=person_list)
    select2 = SelectField('Selecciona el jugador 2', choices=person_list)
    search = SubmitField()

class schedule_form(FlaskForm):
    pass

class signup_coach_form(FlaskForm):
    id = StringField('Correo', validators=[InputRequired(), validate_name])
    password = PasswordField('Contraseña', validators=[InputRequired(), EqualTo('confirm', message='!Passwords must match')])
    confirm = PasswordField('Confirmar contraseña', validators=[InputRequired()])
    name = StringField('Nombre', validators=[InputRequired()])
    lastname = StringField('Apellidos', validators=[InputRequired()])
    birthday = DateField('Cumpleaños', validators=[InputRequired()], format='%Y-%m-%d')
    especialization = StringField('especializacion', validators=[InputRequired()])
    link = StringField('Link profesional', validators=[InputRequired()])
    biography  = TextAreaField('Biografia')
    image = FileField('Foto', validators=[InputRequired()])
    submit = SubmitField()