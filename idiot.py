# -*- coding: utf-8 -*-
"""
    Idiot
    ~~~~~~

    A microblog example application written as Flask tutorial with
    Flask and sqlite3.

    :copyright: (c) 2014 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask_bootstrap import Bootstrap

# create our little application :)
app = Flask(__name__)
Bootstrap(app)
# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'idiot.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
from flask.ext.wtf import Form
from wtforms import StringField, DateField, FloatField, SubmitField, TextAreaField
from wtforms.validators import Required
import datetime

class LoginForm(Form):
    username = StringField('username', validators=[Required()])
    password= StringField('password', validators=[Required()])
    submit = SubmitField('Login')

class PayoutForm(Form):
    username = StringField('username', validators=[Required()])
    apply_money = FloatField('apply_money', validators=[Required()])
    actual_money = FloatField('acutal_money', validators=[Required()])
    note = TextAreaField('note', validators=[Required()])
    submit = SubmitField('Login')

class IncomeForm(Form):
    username = StringField('username', validators=[Required()])
    money = FloatField('money', validators=[Required()])
    note = TextAreaField('note', validators=[Required()])
    submit = SubmitField('Login')
def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


def initdb_commaactual_moneynd():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def index():
    db = get_db()
    cur = db.execute('select * from account order by datetime desc')
    entries = cur.fetchall()
    return render_template('index.html', entries=entries)


@app.route('/payout', methods=['GET', 'POST'])
def payout():
    if not session.get('logged_in'):
        abort(401)

    if request.method == 'POST':
        db = get_db()
        db.execute('insert into account(username, apply_money, actual_money, note, datetime) values (?, ?, ?, ?, ?)',
               [request.form['username'], request.form['apply_money'], request.form['actual_money'], request.form['note'], datetime.datetime.now()])
        db.commit()
        flash('Pay out success! ')
    form = PayoutForm()
    return render_template('payout.html', form=form)

@app.route('/income', methods=['GET', 'POST'])
def income():
    if not session.get('logged_in'):
        abort(401)

    if request.method == 'POST':
        db = get_db()
        db.execute('insert into account(username, apply_money, actual_money, note, datetime) values (?, ?, ?, ?, ?)',
               [request.form['username'], request.form['money'], request.form['money'], request.form['note'], datetime.datetime.now()])
        db.commit()
        flash('Income success!')
    form = IncomeForm()
    return render_template('income.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    form = LoginForm()
    return render_template('login.html', error=error, form=form)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
