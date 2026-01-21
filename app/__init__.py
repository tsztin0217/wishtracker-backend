from flask import Flask
from .db import db, migrate
from .auth import oauth
import os
from .models import user, item, tag, item_tag


def create_app(config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)
    oauth.init_app(app)

    return app