from flask import render_template, redirect, url_for
from flask_login import login_required

from . import profile

@profile.route('/home')
@login_required
def home():
    print('LOGIN')
    return render_template('home.html')

@profile.route('/create')
@login_required
def create():
    return render_template('crud/create.html')