import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import data_required, ValidationError


def email_check(self, email):
    print('HOLA')
    resultado = re.fullmatch('^[a-z]*[.][a-z 0-9]*', email.data)
    if resultado is not None:
        raise ValidationError('El correo no es valido #nombre.apellido00')


class login_form(FlaskForm):
    print('FORMA')
    email = StringField('Email', validators=[data_required(), email_check])
    password = PasswordField('Password', validators=[data_required()])
    submit = SubmitField('Submit')


class signup_form(FlaskForm):
    pass
