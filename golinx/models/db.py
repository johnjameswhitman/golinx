import sqlite3

import flask
from flask import cli

from golinx.models import link_model
from golinx.models import user_model

def get_db():
    if 'db' not in flask.g:
        flask.g.db = sqlite3.connect(
            flask.current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        flask.g.db.row_factory = sqlite3.Row

    return flask.g.db


def close_db(e=None):
    db = flask.g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with flask.current_app.open_resource('models/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    with flask.current_app.open_resource(
            'models/data/seed_users.csv', mode='r') as f:
        for seed_user in user_model.UserModel.from_csv(f, db=db):
            seed_user.save()

    with flask.current_app.open_resource(
            'models/data/seed_links.csv', mode='r') as f:
        for seed_link in link_model.LinkModel.from_csv(f, db=db):
            seed_link.save()


def init_app(app):
    app.teardown_appcontext(close_db)
