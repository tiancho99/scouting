from flask import render_template, redirect, url_for, Markup, session
from flask_login import login_user, logout_user, current_user, login_required

from . import auth
from app.forms import login_form
from app.mysql_service import get_Athlete



@auth.route('/login', methods=['GET', 'POST'])
def login():
    login = login_form()
    
    if login.validate_on_submit:
        email = login.email.data
        password = login.password.data

        user = get_Athlete(email)

        if user and user.check_password(password):
            login_user(user)
            
            return render_template('home.html')
        # return redirect(url_for('profile.home'))

    context = {
        'login_form': login
    }

    return render_template('login.html', **context)

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))