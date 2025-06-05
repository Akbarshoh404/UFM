from flask import Blueprint, request, jsonify
from database_mongo import get_db, generate_id
from datetime import datetime

product_bp = Blueprint('product', __name__)

@product_bp.route('/products', methods=['POST'])
def create_product():
    try:
        data = request.get_json()
        required_fields = ['shopId', 'name', 'description', 'price', 'stock']
        if not all(key in data for key in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        db = get_db()
        shops_collection = db['shops']
        products_collection = db['products']

        # Validate shop exists
        if not shops_collection.find_one({'_id': data['shopId']}):
            return jsonify({'error': 'Shop not found'}), 404

        product_id = generate_id()
        created_at = datetime.utcnow().isoformat()
        updated_at = created_at

        product = {
            '_id': product_id,
            'shopId': data['shopId'],
            'name': data['name'],
            'description': data['description'],
            'price': float(data['price']),
            'stock': int(data['stock']),
            'categories': data.get('categories', []),
            'createdAt': created_at,
            'updatedAt': updated_at
        }

        products_collection.insert_one(product)
        return jsonify({'_id': product_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@product_bp.route('/products', methods=['GET'])
def get_products():
    try:
        db = get_db()
        products_collection = db['products']
        products = list(products_collection.find({}, {
            '_id': 1,
            'shopId': 1,
            'name': 1,
            'description': 1,
            'price': 1,
            'stock': 1,
            'categories': 1,
            'createdAt': 1,
            'updatedAt': 1
        }))
        for product in products:
            product['_id'] = str(product['_id'])
        return jsonify(products), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500