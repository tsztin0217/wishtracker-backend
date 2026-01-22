from flask import Blueprint, session, url_for, redirect, jsonify
from ..auth import oauth
from ..models.user import User
from ..db import db
import os

bp = Blueprint('home_bp', __name__, url_prefix='')

@bp.get('/')
def get_homepage():
    return '<h1>Hello World!</h1>'

@bp.get('/login')
def login():
    redirect_uri = url_for('home_bp.authorize_google', _external=True)
    print(f"[DEBUG] Login redirect_uri: {redirect_uri}")
    print(f"[DEBUG] Session before OAuth: {dict(session)}")
    return oauth.google.authorize_redirect(redirect_uri)

@bp.get('/authorize_google')
def authorize_google():
    try:
        print(f"[DEBUG] Session in callback: {dict(session)}")
        token = oauth.google.authorize_access_token()
        user_info = token.get('userinfo')

        user = User.get_or_create(
            oauth_provider='google',
            oauth_id=user_info['sub'],
            email=user_info['email'],
            name=user_info.get('name')
        )

        session['user_id'] = user.id
        print(f"[DEBUG] Set session['user_id'] = {user.id}")
        print(f"[DEBUG] Session after setting: {dict(session)}")
        
        # Redirect back to frontend
        frontend_url = 'https://wishtracker-frontend-284687348047.us-central1.run.app'
        print(f"[DEBUG] Redirecting to: {frontend_url}")
        return redirect(frontend_url)
    
    except Exception as e:
        print(f"OAuth error: {e}")
        frontend_url = 'https://wishtracker-frontend-284687348047.us-central1.run.app'
        return redirect(f'{frontend_url}?error=auth_failed')

@bp.get('/user')
def get_current_user():
    print(f"[DEBUG] /user endpoint called")
    print(f"[DEBUG] Session in /user: {dict(session)}")
    user_id = session.get('user_id')
    print(f"[DEBUG] user_id from session: {user_id}")
    if not user_id:
        return jsonify({'user': None}), 200
    
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'user': None}), 200
    
    return jsonify({
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'oauth_provider': user.oauth_provider
        }
    }), 200

@bp.post('/logout')
def logout():
    session.clear()
    return jsonify({'message': 'Logged out'}), 200