from flask import Blueprint, session, url_for
from ..auth import oauth

bp = Blueprint('home_bp', __name__, url_prefix='')

@bp.get('/')
def get_homepage():
    user = session.get('user')

@bp.get('/login')
def login():
    redirect_uri = url_for('authorize_google', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@bp.get('/authorize_google')
def authorize_google():
    try:
        token = oauth.google.authorize_access_token()
        user_info = token.get('userinfo')

        user = User.get_or_create