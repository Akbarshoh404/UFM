from flask import Blueprint, request, jsonify
from bson import ObjectId
from datetime import datetime
import bcrypt
from config import db

user_bp = Blueprint('user', __name__)
users = db['users']

def serialize_doc(doc):
    if isinstance(doc, list):
        return [serialize_doc(item) for item in doc]
    if isinstance(doc, dict):
        return {k: str(v) if isinstance(v, ObjectId) else v for k, v in doc.items()}
    return doc

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    required_fields = ['name', 'email', 'password', 'address', 'phone']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    user_data = {
        'name': data['name'],
        'email': data['email'],
        'password': hashed_password.decode('utf-8'),
        'role': data.get('role', 'customer'),
        'address': data['address'],
        'phone': data['phone'],
        'profileImage': data.get('profileImage', ''),
        'createdAt': datetime.utcnow(),
        'updatedAt': datetime.utcnow()
    }
    result = users.insert_one(user_data)
    return jsonify({'_id': str(result.inserted_id)}), 201

@user_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(serialize_doc(user)), 200

@user_bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    update_data = {'updatedAt': datetime.utcnow()}
    for field in ['name', 'email', 'address', 'phone', 'profileImage']:
        if field in data:
            update_data[field] = data[field]
    result = users.update_one({'_id': ObjectId(user_id)}, {'$set': update_data})
    if result.matched_count == 0:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'message': 'User updated'}), 200

@user_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = users.delete_one({'_id': ObjectId(user_id)})
    if result.deleted_count == 0:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'message': 'User deleted'}), 200