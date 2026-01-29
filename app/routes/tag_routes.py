from flask import Blueprint, request, session, jsonify
from app.models.tag import Tag
from app.db import db
from .route_utilities import create_model

import os
bp = Blueprint('tag_bp', __name__, url_prefix='/tags')

@bp.post('')
def create_tag():
    request_data = request.get_json()
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401

    request_data['user_id'] = user_id

    return create_model(Tag, request_data)

@bp.get('')
def get_all_tags():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    tags = Tag.query.filter_by(user_id=user_id).all()
    tags_dict = [tag.to_dict() for tag in tags]

    return jsonify({'tags': tags_dict}), 200

@bp.delete('/<int:tag_id>')
def delete_tag(tag_id):
    user_id = session.get('user_id')
    tag = Tag.query.filter_by(id=tag_id, user_id=user_id).first()
    
    if not tag:
        return jsonify({'error': 'Tag not found'}), 404

    db.session.delete(tag)
    db.session.commit()
    return jsonify({'message': 'Tag deleted successfully'}), 200
