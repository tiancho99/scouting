from flask import render_template, redirect, url_for

from . import profile


@profile.route('/home')
def home():
    print('LOGIN')
    return render_template('home.html')