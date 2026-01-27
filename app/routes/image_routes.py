from flask import Blueprint, jsonify, request, session
from flask_cors import cross_origin
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


@bp.route('/upload-url', methods=['POST', 'OPTIONS'])
@cross_origin(origins=os.getenv('CORS_ORIGINS', '*').split(','), supports_credentials=True)
def get_upload_url():
    """Generate a signed URL for direct upload to GCS"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401

    data = request.get_json()
    filename = data.get('filename')
    content_type = data.get('content_type')

    if not filename or not content_type:
        return jsonify({'error': 'filename and content_type are required'}), 400

    allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    if content_type not in allowed_types:
        return jsonify({'error': 'Invalid image type'}), 400

    try:
        file_uuid = str(uuid.uuid4())
        file_extension = os.path.splitext(filename)[1]
        unique_filename = f"{file_uuid}{file_extension}"
        gcs_path = f"images/{user_id}/{unique_filename}"
        bucket_name = os.getenv('GCS_BUCKET_NAME')
        if not bucket_name:
            return jsonify({'error': 'GCS bucket not configured'}), 500
        client = get_gcs_client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(gcs_path)
        signed_url = blob.generate_signed_url(
            version='v4',
            expiration=timedelta(minutes=15),
            method='PUT',
            content_type=content_type
        )

        return jsonify({
            'upload_url': signed_url,
            'gcs_path': gcs_path,
            'public_url': f"https://storage.googleapis.com/{bucket_name}/{gcs_path}"
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

