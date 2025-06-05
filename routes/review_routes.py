from flask import Blueprint, request, jsonify
from bson import ObjectId
from datetime import datetime
from config import db

review_bp = Blueprint('review', __name__)
product_reviews = db['product_reviews']

def serialize_doc(doc):
    if isinstance(doc, list):
        return [serialize_doc(item) for item in doc]
    if isinstance(doc, dict):
        return {k: str(v) if isinstance(v, ObjectId) else v for k, v in doc.items()}
    return doc

@review_bp.route('/product_reviews', methods=['POST'])
def create_product_review():
    data = request.get_json()
    required_fields = ['user', 'product', 'rating', 'comment']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    review_data = {
        'user': ObjectId(data['user']),
        'product': ObjectId(data['product']),
        'rating': data['rating'],
        'comment': data['comment'],
        'createdAt': datetime.utcnow(),
        'updatedAt': datetime.utcnow()
    }
    result = product_reviews.insert_one(review_data)
    return jsonify({'_id': str(result.inserted_id)}), 201