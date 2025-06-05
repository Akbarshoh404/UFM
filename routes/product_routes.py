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
        'ratingsAverage': data.get('ratingsAverage', 0.0),
        'createdAt': datetime.utcnow().isoformat(),
        'updatedAt': datetime.utcnow().isoformat()
    }
    data_store['products'][product_id] = product_data
    return jsonify({'_id': product_id}), 201

@product_bp.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    product = data_store['products'].get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(serialize_doc(product)), 200