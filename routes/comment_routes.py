from flask import Blueprint, request, jsonify
from bson import ObjectId
from datetime import datetime
from config import db

comment_bp = Blueprint('comment', __name__)
shop_comments = db['shop_comments']

def serialize_doc(doc):
    if isinstance(doc, list):
        return [serialize_doc(item) for item in doc]
    if isinstance(doc, dict):
        return {k: str(v) if isinstance(v, ObjectId) else v for k, v in doc.items()}
    return doc

@comment_bp.route('/shop_comments', methods=['POST'])
def create_shop_comment():
    data = request.get_json()
    required_fields = ['user', 'shop', 'comment']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    comment_data = {
        'user': ObjectId(data['user']),
        'shop': ObjectId(data['shop']),
        'comment': data['comment'],
        'createdAt': datetime.utcnow(),
        'updatedAt': datetime.utcnow()
    }
    result = shop_comments.insert_one(comment_data)
    return jsonify({'_id': str(result.inserted_id)}), 201