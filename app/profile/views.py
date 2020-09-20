from flask import render_template, redirect, url_for, jsonify, request, Markup, flash
from flask_login import login_required, current_user


from . import profile
from app.forms import logout_form, select_position_form, get_versus_form, schedule_form
from app.mysql_service import get_Games, put_Game, get_Person, get_Athletes, get_People, get_stats, get_stats_by_position, get_person_stats
from app.decorators import coach_required

@profile.route('/home/<string:current>')
@login_required
def home(current):
    logout = logout_form()
    schedule = schedule_form()
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
        'schedule': schedule
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
@coach_required
def add_game():
    date = '{} {}'.format(request.form.get('date'),request.form.get('time'))
    location = request.form.get('location')
    training = request.form.get('training')
    
    put_Game(date, location, training=='true')
    user = current_user
    return redirect(url_for('profile.home', current=user.name))

@profile.route('/stats', methods=['GET', 'POST'])
@login_required
def stats():
    # keepers = get_goal_keeper_stats()
    # return Markup('{}'.format(keepers))

    global athletes
    select = select_position_form()
    athletes = get_stats()
    if select.validate_on_submit():
        position = select.position.data
        athletes = get_stats_by_position(position)

        # return render_template('stats.html', **context)    
    context = {
        'select': select,
        'user': current_user,
        'logout': logout_form(),
        'athletes': athletes
    }
    return render_template('stats.html', **context)

@profile.route('/vs', methods=['GET', 'POST'])
@login_required
def versus():
    global players
    players = None

    versus = get_versus_form()

    if versus.validate_on_submit():
        player_selected1 = versus.select1.data
        player_selected2 = versus.select2.data
        if(player_selected1 == player_selected2):
            flash('No puedes comparar el mismo jugador', category="danger")
        else:
            players = get_person_stats(player_selected1, player_selected2)
            if len(players) < 2:
                players = None
                flash('Alguno de los jugadores aun no ha sido calificado', category="danger")
            


        # player3 = get_person_stats('7', '11')
        # return Markup(players[0][0])

    context = {
        'logout': logout_form(),
        'user': current_user,
        'form': versus,
        'players': players,
    }
    return render_template('versus.html', **context)