# -*- coding: utf-8 -*-
"""
    idiot Tests
    ~~~~~~~~~~~~

    Tests the idiot application.

    :copyright: (c) 2014 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

import pytest

import os
import idiot
import tempfile


@pytest.fixture
def client(request):
    db_fd, idiot.app.config['DATABASE'] = tempfile.mkstemp()
    idiot.app.config['TESTING'] = True
    client = idiot.app.test_client()
    with idiot.app.app_context():
        idiot.init_db()

    def teardown():
        os.close(db_fd)
        os.unlink(idiot.app.config['DATABASE'])
    request.addfinalizer(teardown)

    return client


def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def t1est_empty_db(client):
    """Start with a blank database."""
    rv = client.get('/')
    assert b'No entries here so far' in rv.data


def t1est_login_logout(client):
    """Make sure login and logout works"""
    rv = login(client, idiot.app.config['USERNAME'],
               idiot.app.config['PASSWORD'])
    assert b'You were logged in' in rv.data
    rv = logout(client)
    assert b'You were logged out' in rv.data
    rv = login(client, idiot.app.config['USERNAME'] + 'x',
               idiot.app.config['PASSWORD'])
    assert b'Invalid username' in rv.data
    rv = login(client, idiot.app.config['USERNAME'],
               idiot.app.config['PASSWORD'] + 'x')
    assert b'Invalid password' in rv.data


def t1est_messages(client):
    """Test that messages work"""
    login(client, idiot.app.config['USERNAME'],
          idiot.app.config['PASSWORD'])
    rv = client.post('/add', data=dict(
        title='<Hello>',
        text='<strong>HTML</strong> allowed here'
    ), follow_redirects=True)
    assert b'No entries here so far' not in rv.data
    assert b'&lt;Hello&gt;' in rv.data
    assert b'<strong>HTML</strong> allowed here' in rv.data
