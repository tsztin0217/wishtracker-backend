from flask import Flask
from .db import db, migrate
from .auth import oauth
import os
from dotenv import load_dotenv
from .models import user, item, tag, item_tag
from .routes.home_routes import bp as home_bp


load_dotenv()


def create_app(config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)
    oauth.init_app(app)

    app.register_blueprint(home_bp)

    return app