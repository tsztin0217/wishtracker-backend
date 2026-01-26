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