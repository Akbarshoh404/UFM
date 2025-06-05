from flask import Blueprint, request, jsonify
from database_mongo import get_db, generate_id
from datetime import datetime

shop_bp = Blueprint('shop', __name__)

@shop_bp.route('/shops', methods=['POST'])
def create_shop():
    try:
        data = request.get_json()
        required_fields = ['name', 'owner', 'description', 'location']
        if not all(key in data for key in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        db = get_db()
        users_collection = db['users']
        shops_collection = db['shops']

        # Validate owner exists
        if not users_collection.find_one({'_id': data['owner']}):
            return jsonify({'error': 'Owner user not found'}), 404

        shop_id = generate_id()
        created_at = datetime.utcnow().isoformat()
        updated_at = created_at

        shop = {
            '_id': shop_id,
            'name': data['name'],
            'owner': data['owner'],
            'description': data['description'],
            'logo': data.get('logo', ''),
            'location': data['location'],
            'categories': data.get('categories', []),
            'isVerified': False,
            'createdAt': created_at,
            'updatedAt': updated_at
        }

        shops_collection.insert_one(shop)
        return jsonify({'_id': shop_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@shop_bp.route('/shops', methods=['GET'])
def get_shops():
    try:
        db = get_db()
        shops_collection = db['shops']
        shops = list(shops_collection.find({}, {
            '_id': 1,
            'name': 1,
            'owner': 1,
            'description': 1,
            'logo': 1,
            'location': 1,
            'categories': 1,
            'isVerified': 1,
            'createdAt': 1,
            'updatedAt': 1
        }))
        for shop in shops:
            shop['_id'] = str(shop['_id'])
        return jsonify(shops), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500