from flask import Blueprint, request, jsonify
from datetime import datetime
from data_store import data_store, generate_id

comment_bp = Blueprint('comment', __name__)

def serialize_doc(doc):
    return doc

@comment_bp.route('/shop_comments', methods=['POST'])
def create_shop_comment():
    data = request.get_json()
    required_fields = ['user', 'shop', 'comment']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    comment_id = generate_id()
    comment_data = {
        '_id': comment_id,
        'user': data['user'],
        'shop': data['shop'],
        'comment': data['comment'],
        'createdAt': datetime.utcnow().isoformat(),
        'updatedAt': datetime.utcnow().isoformat()
    }
    data_store['shop_comments'][comment_id] = comment_data
    return jsonify({'_id': comment_id}), 201