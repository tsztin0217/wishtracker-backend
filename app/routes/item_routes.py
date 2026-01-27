from flask import Blueprint, request, make_response, abort, Response, session, jsonify
from app.models.item import Item
from app.models.tag import Tag
from app.models.item_tag import ItemTag
from app.db import db
from .route_utilities import create_model
from google.cloud import storage
import os
bp = Blueprint('item_bp', __name__, url_prefix='/items')

@bp.post('')
def create_item():
    request_data = request.get_json()
    print("Received data:", request_data)
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401

    request_data['user_id'] = user_id

    return create_model(Item, request_data)

@bp.get('')
def get_all_items():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    items = Item.query.filter_by(user_id=user_id).all()
    items_dict = [item.to_dict() for item in items]
    return make_response({'items': items_dict}, 200)

@bp.delete('/<int:item_id>')
def delete_item(item_id):
    """Delete an item and its associated image from GCS."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    item = Item.query.filter_by(id=item_id, user_id=user_id).first()
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    gcs_path = item.gcs_path
    bucket_name = os.getenv('GCS_BUCKET_NAME')
    if gcs_path and bucket_name:
        try:
            client = storage.Client()
            bucket = client.bucket(bucket_name)
            blob = bucket.blob(gcs_path)
            if blob.exists():
                blob.delete()
        except Exception as e:
            print(f"[ERROR] Failed to delete image from GCS: {e}")
    try:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item and image deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500