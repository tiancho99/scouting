from flask import render_template, redirect, url_for, jsonify
from flask_login import login_required, current_user


from . import profile
from app.forms import logout_form
from app.mysql_service import get_Games


@profile.route('/home/<string:current>')
@login_required
def home(current):
    logout = logout_form()
    user = current_user
    games = get_Games()
    print(games)
    for game in games:
        jsonify({'game': game})

    if logout.validate_on_submit():
        return redirect(url_for('auth.logout'))
        
    context = {
        'user': user,
        'logout': logout,
        # 'games': games,
    }
    return render_template('home.html', **context)

