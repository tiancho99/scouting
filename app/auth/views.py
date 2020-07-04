from flask import render_template, redirect, url_for, Markup, session, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
import os 

from . import auth
from app.models import Athlete
from app.forms import login_form, signup_form
from app.mysql_service import get_Athlete, put_Athlete




@auth.route('/login', methods=['GET', 'POST'])
def login():
    login = login_form()

    if login.validate_on_submit():
        email = login.email.data
        password = login.password.data

        user = get_Athlete(email)

        if user and user.check_password(password):
            login_user(user)
            flash('Logued in successfully', category="success")
            return redirect(url_for('profile.home'))
        # return redirect(url_for('profile.home'))

    context = {
        'login_form': login
    }

    return render_template('login.html', **context)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    signup = signup_form()

    if signup.validate_on_submit():
        email = signup.id.data
        user = get_Athlete(email)

        if user is None:
            email = signup.id.data
            password = signup.password.data
            name = signup.name.data
            lastname = signup.lastname.data
            height = signup.height.data
            weight = signup.weight.data
            birthday = signup.birthday.data
            dorsal = signup.dorsal.data
            position = signup.position.data
            image = signup.image.data
            print(image)
            if image != '':
                image_name = secure_filename(email+'_'+image.filename)
                image_path = os.path.abspath('app/static/uploads/{}'.format(image_name))
                image.save(image_path)
                put_Athlete(email, password, name, lastname, height, weight, birthday, dorsal, position, image_path)
            else:
                put_Athlete(email, password, name, lastname, height, weight, birthday, dorsal, position, None)

            flash('User successfully registered', category='success')
            user = Athlete(email, name, lastname, height, weight, birthday, dorsal, position, False, image_path)
            login_user(user)
            return redirect(url_for('profile.home'))
        else:
            flash('User already exist', category='danger')
    else:
       if request.method == 'POST':
            flash('Something went wrong, check the fields', category='danger')

    context = {
        'signup_form': signup
    }
    return render_template('signup.html', **context)


@auth.route('/logout', methods=['GET', 'POST'])

@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))