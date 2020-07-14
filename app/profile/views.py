from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from . import profile


@profile.route('/home')
@login_required
def home():
    user = current_user
    context = {
        'user': user
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