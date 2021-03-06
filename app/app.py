#!/usr/bin/env python3
# coding: utf-8
# pylint: disable=C0103,C0111,R0201,E1101
# Romain Vincent, GetWatuAsk
"""Routes for the app."""

import datetime as dt
import smtplib
from flask import Flask, redirect, url_for, request, render_template, session

import data_query as db


app = Flask(__name__, static_url_path='/static')
app.secret_key = 'Ts2V+eDAwCK/gZLoe+KhyUjgpnBrHE3yumYuuRG59Q4='
app.config['TEMPLATES_AUTO_RELOAD'] = True


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


@app.route('/needs', methods=['GET', 'POST'])
def get_needs():
    user_id = session['user']['user_id']
    user = db.get_user_by_id(user_id)
    if user is None:
        msg = "Couldn't get user N°{}".format(user_id)
        return render_template('403.html', msg=msg, route='get_needs'), 403

    args = {'states': list()}
    args['states'].append(request.form.get('open'))
    args['states'].append(request.form.get('win'))
    args['states'].append(request.form.get('lost'))

    args['min_date'] = request.form.get('min_date')
    args['max_date'] = request.form.get('max_date')
    args['client_name'] = request.form.get('client_name')
    args['title'] = request.form.get('title')

    needs = db.get_needs_from_user(user_id, args)

    if needs is None:
        msg = "Couldn't get needs for user N°{}".format(user_id)
        return render_template('403.html', msg=msg, route='get_needs'), 403

    for need in needs:
        need['remaining'] = (need['latest_date'] - need['creation_date']).days

    return render_template('need-list.html', user=user, needs=needs, clients=db.get_clients(), total=len(needs)), 200


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
        msg = "Couldn't get need N°{}".format(need_id)
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

        user = session['user']
        client = db.get_client_by_id(need['client_id'])

        return render_template('edit-need.html', need=need, user=user, client=client), 200

    elif request.method == 'POST':
        description = request.form.get('description')
        consultant_name = request.form.get('consultant_name')
        keys = request.form.get('keys')
        latest_date = request.form.get('dueDate')
        month = request.form.get('month')
        day = request.form.get('day')
        price_ht = request.form.get('price_ht')
        status_id = request.form.get('selectStatus')

        need = db.get_need_by_id(need_id)
        print("EDIT-NEED before edit : ", need)
        db.update_need(need_id, description, latest_date, month,
                       day, price_ht, consultant_name, status_id, keys)

        return redirect(url_for('get_needs'))
    else:
        return "Not implemented yet", 404


def camelcasify(string):
    words = [word.title() if i != 0 else word
             for i, word in enumerate(string.split(' '))]
    return "".join(words)


@app.route('/needs/new', methods=['GET', 'POST'])
def new_need():
    if request.method == 'GET':
        params = {'consultant_name': request.args.get('consultant_name'),
                  'user_id': session['user']['user_id'],
                  'today': dt.date.today()}

        clients = db.get_clients()
        params['clients'] = clients
        user = session['user']

        return render_template('new-need.html', params=params, user=user), 200

    # Method POST:
    new_need = request.form.to_dict()
    if 'title' in new_need:
        new_need['title'] = camelcasify(new_need['title'])
    session['user']['last_insert_need_id'] = db.insert_need(new_need)

    # send_mail()
    return redirect(url_for('get_needs'), code=302)


@app.route('/needs/delete/<need_id>', methods=['GET', 'POST'])
def delete_need(need_id):
    if request.method == 'POST':
        db.delete_need(need_id)
        return redirect(url_for('get_needs'))
    return "Not implemented yet", 404


def send_mail():
    print("PASSE PAR LA")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("workshop.epsi.btrois@gmail.com", "Azqswx21!")

    msg = "Creation d'un nouveau besoin à votre nom. Vous pouvez le retrouver dans la liste de vos besoins."
    try:
        server.sendmail("workshop.epsi.btrois@gmail.com",
                        "workshop.epsi.btrois@gmail.com", msg)
    except:
        print("Impossible d'envoyer le mail!")
    server.quit()


if __name__ == '__main__':
    app.run(debug=True)
