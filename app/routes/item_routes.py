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
    raw_user_id = session.get('user_id') or request.headers.get('X-User-ID')
    user_id = int(raw_user_id) if raw_user_id else None
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401

    # separate tags from the main item data
    tag_data = request_data.pop('tags', [])
    request_data['user_id'] = user_id

    # create item first
    new_item = Item.from_dict(request_data)
    
    # associate tags (many-to-nany)
    for t in tag_data:
        tag_name = t['name'] if isinstance(t, dict) else t
        # check if this user already has a tag with this name
        tag = Tag.query.filter_by(name=tag_name, user_id=user_id).first()
        if not tag:
            tag = Tag(name=tag_name, user_id=user_id)
            db.session.add(tag)
        
        new_item.tags.append(tag)

    db.session.add(new_item)
    db.session.commit()
    return jsonify(new_item.to_dict()), 201


@bp.get('')
def get_all_items():
    raw_user_id = session.get('user_id') or request.headers.get('X-User-ID')
    user_id = int(raw_user_id) if raw_user_id else None
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    items = Item.query.filter_by(user_id=user_id).order_by(Item.created_at.asc()).all()
    items_dict = [item.to_dict() for item in items]
    return make_response({'items': items_dict}, 200)

@bp.delete('/<int:item_id>')
def delete_item(item_id):
    """Delete an item and its associated image from GCS."""
    raw_user_id = session.get('user_id') or request.headers.get('X-User-ID')
    user_id = int(raw_user_id) if raw_user_id else None
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

@bp.patch('/<int:item_id>')
def update_item(item_id):
    raw_user_id = session.get('user_id') or request.headers.get('X-User-ID')
    user_id = int(raw_user_id) if raw_user_id else None
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    item = Item.query.filter_by(id=item_id, user_id=user_id).first()
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    request_data = request.get_json()
    tag_data = request_data.pop('tags', None)
    
    item.name = request_data.get('name', item.name)
    item.description = request_data.get('description', item.description)
    item.price = request_data.get('price', item.price)
    
    # update timestamp for last_updated
    from datetime import datetime, timezone
    item.last_updated = datetime.now(timezone.utc)

    # update tags if provided
    if tag_data is not None:
        item.tags.clear()
        for t in tag_data:
            tag_name = t['name'] if isinstance(t, dict) else t
            tag = Tag.query.filter_by(name=tag_name, user_id=user_id).first()
            if not tag:
                tag = Tag(name=tag_name, user_id=user_id)
                db.session.add(tag)
            item.tags.append(tag)
    
    db.session.commit()
    return jsonify(item.to_dict()), 200