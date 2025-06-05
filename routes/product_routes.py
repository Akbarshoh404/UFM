from flask import Blueprint, request, jsonify
from bson import ObjectId
from datetime import datetime
from config import db

product_bp = Blueprint('product', __name__)
products = db['products']

def serialize_doc(doc):
    if isinstance(doc, list):
        return [serialize_doc(item) for item in doc]
    if isinstance(doc, dict):
        return {k: str(v) if isinstance(v, ObjectId) else v for k, v in doc.items()}
    return doc

@product_bp.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    required_fields = ['shop', 'name', 'price', 'description', 'category']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    product_data = {
        'shop': ObjectId(data['shop']),
        'name': data['name'],
        'images': data.get('images', []),
        'price': data['price'],
        'description': data['description'],
        'size': data.get('size', []),
        'color': data.get('color', []),
        'stock': data.get('stock', 0),
        'category': data['category'],
        'ratingsAverage': data.get('ratingsAverage', 0.0),
        'createdAt': datetime.utcnow(),
        'updatedAt': datetime.utcnow()
    }
    result = products.insert_one(product_data)
    return jsonify({'_id': str(result.inserted_id)}), 201

@product_bp.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    product = products.find_one({'_id': ObjectId(product_id)})
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(serialize_doc(product)), 200