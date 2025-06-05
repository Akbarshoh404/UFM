from flask import Blueprint, request, jsonify
from bson import ObjectId
from datetime import datetime
from config import db

shop_bp = Blueprint('shop', __name__)
shops = db['shops']

def serialize_doc(doc):
    if isinstance(doc, list):
        return [serialize_doc(item) for item in doc]
    if isinstance(doc, dict):
        return {k: str(v) if isinstance(v, ObjectId) else v for k, v in doc.items()}
    return doc

@shop_bp.route('/shops', methods=['POST'])
def create_shop():
    data = request.get_json()
    required_fields = ['name', 'owner', 'description', 'location']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    shop_data = {
        'name': data['name'],
        'owner': ObjectId(data['owner']),
        'description': data['description'],
        'logo': data.get('logo', ''),
        'location': data['location'],
        'categories': data.get('categories', []),
        'isVerified': data.get('isVerified', False),
        'createdAt': datetime.utcnow(),
        'updatedAt': datetime.utcnow()
    }
    result = shops.insert_one(shop_data)
    return jsonify({'_id': str(result.inserted_id)}), 201

@shop_bp.route('/shops/<shop_id>', methods=['GET'])
def get_shop(shop_id):
    shop = shops.find_one({'_id': ObjectId(shop_id)})
    if not shop:
        return jsonify({'error': 'Shop not found'}), 404
    return jsonify(serialize_doc(shop)), 200