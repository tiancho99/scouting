from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from . import profile
from app.forms import logout_form


@profile.route('/home')
@login_required
def home():
    logout = logout_form()
    user = current_user
    
    if logout.validate_on_submit():
        return redirect(url_for('auth.logout'))
        
    context = {
        'user': user,
        'logout': logout
    }
    return render_template('home.html', **context)

@profile.route('/read')
@login_required
def read():
    return render_template('crud/read.html')

@profile.route('/update')
@login_required
def update():
    return render_template('crud/update.html')

@profile.route('/delete')
@login_required
def delete():
    return render_template('crud/delete.html')