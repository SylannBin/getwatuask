#!/usr/bin/env python3
# coding: utf-8
# pylint: disable=C0103,C0111,R0201,E1101
# Romain Vincent, GetWatuAsk
"""Routes for the app."""

import datetime as dt

from flask import Flask, redirect, url_for, request, render_template, session

import data_query as db

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'Ts2V+eDAwCK/gZLoe+KhyUjgpnBrHE3yumYuuRG59Q4='


@app.route('/')
def index():
    return redirect(url_for('login'), code=302)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html'), 200

    # Method POST
    user_email = request.form.get('inputMail')
    password = request.form.get('inputPassword')

    if not (user_email and password):
        return "Unprocessable Entity", 422

    user = db.login(user_email)
    if user is None or not (user['mail'] == user_email and
                            user['password'] == password):
        msg = "Invalid email or password"
        return render_template('403.html', msg=msg, route='login'), 403

    # Connected, redirect to index
    session['user'] = user
    return redirect(url_for('get_needs', user_id=user['user_id']), code=302)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'), code=302)

@app.route('/needs')
def get_needs():
    user_id = session['user']['user_id']
    user = db.get_user_by_id(user_id)
    if user is None:
        msg = "Couldn't get user N°" + user_id
        return render_template('403.html', msg=msg, route='get_needs'), 403

    needs = db.get_needs_from_user(user_id)

    if needs is None:
        msg = "Couldn't get needs for user N°" + user_id
        return render_template('403.html', msg=msg, route='get_needs'), 403

    for need in needs:
        need['remaining'] = (need['latest_date'] - need['creation_date']).days

    return render_template('need-list.html', user=user, needs=needs, total=len(needs)), 200


@app.route('/filtered_needs', methods=['GET', 'POST'])
def get_filtered_needs():

    user_id = session['user']['id_user']
    user = db.get_user_by_id(user_id)
    filters = ""

    states_list = []
    # Method POST
    if request.form.get('open'):
        states_list.append(1)
    if request.form.get('win'):
        states_list.append(2)
    if request.form.get('lost'):
        states_list.append(3)

    states = tuple(states_list)
    filters += "AND id_status IN ", states

    create_date = request.form.get('initialDate')
    latest_date = request.form.get('dueDate')
    client_name = request.form.get('clientName')
    title_need = request.form.get('titleNeed')

    if create_date:
        filters += " AND creation_date = '", create_date, "' "

    if latest_date:
        filters += " AND latest_date = '", latest_date, "' "

    if client_name:
        filters += " AND c_name ILIKE '%", client_name, "%' "

    if title_need:
        filters += " AND title ILIKE '%", title_need, "%' "

    filtered_needs = db.get_filter_needs(filters, user_id)

    if user is None:
        msg = "Couldn't get user N°" + user_id
        return render_template('403.html', msg=msg, route='get_needs'), 403


    if filtered_needs is None:
        msg = "Couldn't find filtered needs."
        return render_template('403.html', msg=msg, route='get_needs'), 403

    for need in filtered_needs:
        need['remaining'] = (need['release'] - need['date']).days

    return render_template('need-list.html', user=user, needs=filtered_needs), 2007






@app.route('/client/<client_id>/<need_id>/<qr_code_salt>')
def client_need(client_id, need_id, qr_code_salt):
    ok = qr_code_salt is not None  # We should check the code
    client = db.get_client_by_id(client_id)
    needs = db.get_needs_id(client_id)
    need = db.get_need_by_id(need_id)
    return render_template('client-dashboard.html', client=client, need=need,
                           need_ids=needs), 200


@app.route('/needs/view/<need_id>')
def view_need(need_id):
    need = db.get_need_by_id(need_id)
    if need is None:
        msg = "Couldn't get need N°" + need_id
        return render_template('403.html', msg=msg, route='get_needs'), 403

    return render_template('view.html', need=need), 200


@app.route('/needs/edit/<need_id>', methods=['GET', 'POST'])
def edit_need(need_id=None):
    if request.method == 'GET':
        # Reload from session or get directly from database
        if need_id is not None:
            need = db.get_need_by_id(need_id)
            session['need'] = need
        elif session['need'] is not None:
            need = session['need']
        else:
            return "unprocessable entity", 422

        if need is None:
            msg = "Couldn't get need N°" + need_id
            return render_template('403.html', msg=msg, route='edit_need'), 403

        return render_template('need-form.html', need=need), 200

    # Method POST
    # TODO: Handle form data to edit the need in db
    request.form.get('data')

    if need is None:
        msg = "Couldn't get need N°" + need_id
        return render_template('403.html', msg=msg, route='edit_need'), 403

    return "Not implemented yet", 404


# GET Argument: manager_name
# POST body: 'NEED' form data
@app.route('/needs/new', methods=['GET', 'POST'])
def new_need():
    if request.method == 'GET':
        # BONUS: request.args.get('token') token must be valid (manager or admin)
        params = {'manager': request.args.get('manager_name'),
                  'date': dt.date.today()}
        return render_template('need-form.html', params=params), 200
    # TODO: Handle form data to create a new need in db
    return "Not implemented yet", 404


if __name__ == '__main__':
    app.run(debug=True)
