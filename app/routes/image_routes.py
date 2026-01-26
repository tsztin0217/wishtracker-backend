from flask import Blueprint, jsonify, request, session
from google.cloud import storage
import os
import uuid
from datetime import timedelta
bp = Blueprint('images_bp', __name__, url_prefix='/api/images')

def get_gcs_client():
    credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if credentials_path:
        if not os.path.isabs(credentials_path):
            credentials_path = os.path.join(os.path.dirname(__file__), credentials_path)
        if os.path.exists(credentials_path):
            return storage.Client.from_service_account_json(credentials_path)
    return storage.Client()

