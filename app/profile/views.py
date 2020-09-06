from flask import render_template, redirect, url_for, jsonify, request, Markup
from flask_login import login_required, current_user


from . import profile
from app.forms import logout_form, select_position
from app.mysql_service import get_Games, put_Game, get_Person, get_Athletes, get_People, get_stats,get_stats_by_position


@profile.route('/home/<string:current>')
@login_required
def home(current):
    logout = logout_form()
    user = current_user
    game_form_url = url_for('profile.add_game')
    athletes = get_Person

    if logout.validate_on_submit():
        return redirect(url_for('auth.logout'))
        
    context = {
        'user': user,
        'logout': logout,
        'games': games,
        'game_form_url': game_form_url,
    }
    return render_template('home.html', **context)

@profile.route('/games')
@login_required
def games():
    games = get_Games()
    if games:
        return games

@profile.route('/add_game', methods=['POST'])
@login_required
def add_game():
    date = '{} {}'.format(request.form.get('date'),request.form.get('time'))
    location = request.form.get('location')
    training = request.form.get('training')
    
    put_Game(date, location, training=='true')
    user = current_user
    return redirect(url_for('profile.home', current=user.name))

@profile.route('/stats')
@login_required
def stats():
    # stat = get_stats()
    # return '<p>\{}</p>'.format(stat)
    select = select_position()
    athletes = get_stats_by_position(1)
    context = {
        'select': select,
        'user': current_user,
        'logout': logout_form(),
        'athletes': athletes
    }
    return render_template('stats.html', **context)