from flask import Flask
from flask_cors import CORS
from .db import db, migrate
from .auth import oauth
import os
from dotenv import load_dotenv
from .models import users, item, tag, item_tag
from .routes.home_routes import bp as home_bp
from werkzeug.middleware.proxy_fix import ProxyFix
from google.cloud.sql.connector import Connector, IPTypes

load_dotenv()

def create_app(config=None):
    app = Flask(__name__)
    
    # 1. Database Connection Logic
    db_uri = os.getenv('SQLALCHEMY_DATABASE_URI', '')
    # Detect production vs local migration attempt
    is_production = '/cloudsql/' in db_uri or os.getenv('FLASK_ENV') == 'production'

    if is_production:
        # Production: Use the Unix Socket path from your .env
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    else:
        # Local: Use Python Connector to bridge to Cloud SQL
        connector = Connector()
        def getconn():
            return connector.connect(
                os.getenv("CLOUD_SQL_INSTANCE_NAME"), 
                "pg8000",
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASS"),
                db=os.getenv("DB_NAME"),
                ip_type=IPTypes.PUBLIC
            )
        app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+pg8000://"
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"creator": getconn}

    # 2. General Config
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['AUTHLIB_INSECURE_TRANSPORT'] = not is_production

    # 3. Session & Security
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    allowed_origins = os.getenv('CORS_ORIGINS', '*').split(',')
    CORS(app, origins=allowed_origins, supports_credentials=True)
    
    if is_production:
        app.config['SESSION_COOKIE_SECURE'] = True
        app.config['SESSION_COOKIE_HTTPONLY'] = True
        app.config['SESSION_COOKIE_SAMESITE'] = 'None'

    if config:
        app.config.update(config)

    # 4. Initialization
    db.init_app(app)
    migrate.init_app(app, db)
    oauth.init_app(app)
    app.register_blueprint(home_bp)

    return app
