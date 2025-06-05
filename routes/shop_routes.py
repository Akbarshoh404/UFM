from flask import Blueprint, request, jsonify
from datetime import datetime
from data_store import data_store, generate_id

shop_bp = Blueprint('shop', __name__)

def serialize_doc(doc):
    return doc

@shop_bp.route('/shops', methods=['POST'])
def create_shop():
    data = request.get_json()
    required_fields = ['name', 'owner', 'description', 'location']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    shop_id = generate_id()
    shop_data = {
        '_id': shop_id,
        'name': data['name'],
        'owner': data['owner'],
        'description': data['description'],
        'logo': data.get('logo', ''),
        'location': data['location'],
        'categories': data.get('categories', []),
        'isVerified': data.get('isVerified', False),
        'createdAt': datetime.utcnow().isoformat(),
        'updatedAt': datetime.utcnow().isoformat()
    }
    data_store['shops'][shop_id] = shop_data
    return jsonify({'_id': shop_id}), 201

@shop_bp.route('/shops/<shop_id>', methods=['GET'])
def get_shop(shop_id):
    shop = data_store['shops'].get(shop_id)
    if not shop:
        return jsonify({'error': 'Shop not found'}), 404
    return jsonify(serialize_doc(shop)), 200