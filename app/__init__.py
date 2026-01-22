from flask import Flask
from flask_cors import CORS
from .db import db, migrate
from .auth import oauth
import os
from dotenv import load_dotenv
from .models import user, item, tag, item_tag
from .routes.home_routes import bp as home_bp
from werkzeug.middleware.proxy_fix import ProxyFix


load_dotenv()


def create_app(config=None):
    app = Flask(__name__)
    
    # Trust proxy headers from Cloud Run
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # Get allowed origins from environment
    allowed_origins = os.getenv('CORS_ORIGINS').split(',')
    CORS(app, origins=allowed_origins, supports_credentials=True)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Session configuration for cross-origin cookies
    # Detect production by checking for Cloud SQL or run.app or explicit env var
    is_production = (
        '/cloudsql/' in os.getenv('SQLALCHEMY_DATABASE_URI', '') or 
        'run.app' in os.getenv('SQLALCHEMY_DATABASE_URI', '') or
        os.getenv('FLASK_ENV') == 'production'
    )
    
    print(f"[DEBUG] is_production: {is_production}")
    print(f"[DEBUG] DB URI contains cloudsql: {'/cloudsql/' in os.getenv('SQLALCHEMY_DATABASE_URI', '')}")
    
    if is_production:
        app.config['SESSION_COOKIE_SECURE'] = True
        app.config['SESSION_COOKIE_HTTPONLY'] = True
        app.config['SESSION_COOKIE_SAMESITE'] = 'None'
        print("[DEBUG] Production session cookie config applied")
    
    # For OAuth state parameter
    app.config['AUTHLIB_INSECURE_TRANSPORT'] = not is_production

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)
    oauth.init_app(app)

    app.register_blueprint(home_bp)

    return app