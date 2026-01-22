from flask import Flask
from flask_cors import CORS
from .db import db, migrate
from .auth import oauth
import os
from dotenv import load_dotenv
from .models import user, item, tag, item_tag
from .routes.home_routes import bp as home_bp


load_dotenv()


def create_app(config=None):
    app = Flask(__name__)

    # Get allowed origins from environment
    allowed_origins = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')
    CORS(app, origins=allowed_origins, supports_credentials=True)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Session configuration for cross-origin cookies in production
    is_production = 'run.app' in os.getenv('SQLALCHEMY_DATABASE_URI', '')
    if is_production:
        app.config['SESSION_COOKIE_SECURE'] = True
        app.config['SESSION_COOKIE_HTTPONLY'] = True
        app.config['SESSION_COOKIE_SAMESITE'] = 'None'
        app.config['SESSION_COOKIE_DOMAIN'] = None  # Don't set domain for Cloud Run
    
    # For OAuth state parameter
    app.config['AUTHLIB_INSECURE_TRANSPORT'] = not is_production

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)
    oauth.init_app(app)

    app.register_blueprint(home_bp)

    return app