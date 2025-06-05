from flask import Blueprint, request, jsonify
from datetime import datetime
from data_store import data_store, generate_id

review_bp = Blueprint('review', __name__)

def serialize_doc(doc):
    return doc

@review_bp.route('/product_reviews', methods=['POST'])
def create_product_review():
    data = request.get_json()
    required_fields = ['user', 'product', 'rating', 'comment']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    review_id = generate_id()
    review_data = {
        '_id': review_id,
        'user': data['user'],
        'product': data['product'],
        'rating': data['rating'],
        'comment': data['comment'],
        'createdAt': datetime.utcnow().isoformat(),
        'updatedAt': datetime.utcnow().isoformat()
    }
    data_store['product_reviews'][review_id] = review_data
    return jsonify({'_id': review_id}), 201