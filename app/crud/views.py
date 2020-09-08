from flask import render_template, url_for, request, Markup, flash, redirect
from flask_login import current_user, login_required
from datetime import datetime

from . import crud
from app.forms import logout_form, create_edit_form, search_person_form, edit_form, delete_person_form, assess_form
from app.mysql_service import get_Person, put_Athlete, get_People, update_Athlete, delete_Person

@crud.route('/view', methods=['GET', 'POST'])
@login_required
def view():
    logout = logout_form()
    search = search_person_form()

    if search.validate_on_submit():
        id = search.player.data
        player = get_Person(id)
        edit = create_edit_form(id=id)
        
        context = {
            'user': current_user,
            'player': player,
            'logout':logout,
            'search': search,
            'edit': edit,
            
        }
        return render_template('view.html', **context)

    context = {
        'user': current_user,
        'logout': logout,
        'search': search,
    }
    return render_template('view.html', **context)

@crud.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = edit_form(request.form)
    id = form.id.data
    email = form
    if request.method == 'POST' and form.validate():
        player = get_Person(email)
        email
        if player is None:
            # insert
            email = form.email.data
        name = form.name.data
        lastname = form.lastname.data
        birthday = form.birthday.data
        height = form.height.data
        weight = form.weight.data
        dorsal = form.dorsal.data
        position = form.position.data
        update_Athlete(id, email, name, lastname, birthday, height, weight, dorsal, position)
        flash('User update successfuly', category='success') 
    else:
        flash('Something went wrong, check the fields', category='danger')
    return redirect(url_for('crud.view'))
    

@crud.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    logout = logout_form()
    delete = delete_person_form()

    if delete.validate_on_submit():
        id = delete.player.data
        player = get_Person(id)

        if player is not None:
            delete_Person(player)
            flash('User delete successfuly', category='success') 
        
    context = {
        'user': current_user,
        'logout': logout,
        'delete': delete,
    }
    return render_template('delete.html', **context)

@crud.route('/assess', methods=['GET', 'POST'])
@login_required
def assess():
    logout = logout_form()
    assess = assess_form()
    if request.args:
        year = request.args.get('year')
        month = request.args.get('month')
        day = request.args.get('day')
        hour = request.args.get('hour')
        date_str = '{}-{}-{} {}:00'.format(year, month, day, hour)
        date = datetime.strptime(date_str,'%Y-%m-%d %H:%M:%S')
        assess.matches.default = date
        assess.process()
    print(assess.validate_on_submit())

    if assess.validate_on_submit():
        return Markup('hola')
        player = assess.player.player.data
        match = match.matches.data
        played_time = assess.played_time.data
        saves = assess.saves.data
        clearances = assess.clearances.data
        centered_passes = assess.centered_passes.data
        assists = assess.assists.data
        interceptions = assess.interceptions.data
        short_passes = assess.short_passes.data
        long_passes = assess.long_passes.data
        scored_goals = assess.scored_goals.data
        scored_penalties = assess.scored_penalties.data
        scored_freekicks = assess.saves.data
        return Markup(assess.matches.data)


    context = {
        'assess': assess,
        'user': current_user,
        'logout': logout
    }

    return render_template('assess.html', **context)