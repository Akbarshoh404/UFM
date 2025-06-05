from flask import Blueprint, request, jsonify
from datetime import datetime
from data_store import data_store, generate_id, hash_password

user_bp = Blueprint('user', __name__)

def serialize_doc(doc):
    return doc

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    required_fields = ['name', 'email', 'password', 'address', 'phone']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    user_id = generate_id()
    user_data = {
        '_id': user_id,
        'name': data['name'],
        'email': data['email'],
        'password': hash_password(data['password']),
        'role': data.get('role', 'customer'),
        'address': data['address'],
        'phone': data['phone'],
        'profileImage': data.get('profileImage', ''),
        'createdAt': datetime.utcnow().isoformat(),
        'updatedAt': datetime.utcnow().isoformat()
    }
    data_store['users'][user_id] = user_data
    return jsonify({'_id': user_id}), 201

@user_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = data_store['users'].get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(serialize_doc(user)), 200

@user_bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id not in data_store['users']:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    update_data = {'updatedAt': datetime.utcnow().isoformat()}
    for field in ['name', 'email', 'address', 'phone', 'profileImage']:
        if field in data:
            update_data[field] = data[field]
    
    data_store['users'][user_id].update(update_data)
    return jsonify({'message': 'User updated'}), 200

@user_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in data_store['users']:
        return jsonify({'error': 'User not found'}), 404
    
    del data_store['users'][user_id]
    return jsonify({'message': 'User deleted'}), 200