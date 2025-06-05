from flask import Blueprint, request, jsonify
from datetime import datetime
from data_store import data_store, generate_id

product_bp = Blueprint('product', __name__)

def serialize_doc(doc):
    return doc

@product_bp.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    required_fields = ['shop', 'name', 'price', 'description', 'category']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if data['shop'] not in data_store['shops']:
        return jsonify({'error': 'Shop not found'}), 404
    
    product_id = generate_id()
    product_data = {
        '_id': product_id,
        'shop': data['shop'],
        'name': data['name'],
        'images': data.get('images', []),
        'price': data['price'],
        'description': data['description'],
        'size': data.get('size', []),
        'color': data.get('color', []),
        'stock': data.get('stock', 0),
        'category': data['category'],
        'reviews': [],  # Embedded reviews list
        'ratingsAverage': data.get('ratingsAverage', 0.0),
        'createdAt': datetime.utcnow().isoformat(),
        'updatedAt': datetime.utcnow().isoformat()
    }
    data_store['products'][product_id] = product_data
    return jsonify({'_id': product_id}), 201

@product_bp.route('/products', methods=['GET'])
def get_all_products():
    products = list(data_store['products'].values())
    return jsonify(serialize_doc(products)), 200

@product_bp.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    product = data_store['products'].get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(serialize_doc(product)), 200

@product_bp.route('/products/<product_id>/reviews', methods=['POST'])
def create_product_review(product_id):
    if product_id not in data_store['products']:
        return jsonify({'error': 'Product not found'}), 404
    
    data = request.get_json()
    required_fields = ['user', 'rating', 'comment']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if data['user'] not in data_store['users']:
        return jsonify({'error': 'User not found'}), 404
    
    review_id = generate_id()
    review_data = {
        '_id': review_id,
        'user': data['user'],
        'rating': data['rating'],
        'comment': data['comment'],
        'createdAt': datetime.utcnow().isoformat(),
        'updatedAt': datetime.utcnow().isoformat()
    }
    data_store['products'][product_id]['reviews'].append(review_data)
    
    # Update ratingsAverage
    reviews = data_store['products'][product_id]['reviews']
    ratings = [r['rating'] for r in reviews]
    data_store['products'][product_id]['ratingsAverage'] = sum(ratings) / len(ratings) if ratings else 0.0
    
    return jsonify({'_id': review_id}), 201