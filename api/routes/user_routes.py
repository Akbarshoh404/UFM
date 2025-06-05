from flask import Blueprint, request, jsonify
from database_mongo import get_db, generate_id, hash_password
from datetime import datetime

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        required_fields = ['username', 'email', 'password']
        if not all(key in data for key in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        db = get_db()
        users_collection = db['users']

        # Check for duplicate username or email
        if users_collection.find_one({'username': data['username']}):
            return jsonify({'error': 'Username already exists'}), 409
        if users_collection.find_one({'email': data['email']}):
            return jsonify({'error': 'Email already exists'}), 409

        user_id = generate_id()
        created_at = datetime.utcnow().isoformat()
        updated_at = created_at

        user = {
            '_id': user_id,
            'username': data['username'],
            'email': data['email'],
            'password': hash_password(data['password']),
            'role': data.get('role', 'user'),  # Default to 'user'
            'createdAt': created_at,
            'updatedAt': updated_at
        }

        users_collection.insert_one(user)
        return jsonify({'_id': user_id, 'username': user['username'], 'email': user['email']}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users', methods=['GET'])
def get_users():
    try:
        db = get_db()
        users_collection = db['users']
        users = list(users_collection.find({}, {
            '_id': 1,
            'username': 1,
            'email': 1,
            'role': 1,
            'createdAt': 1,
            'updatedAt': 1
        }))
        for user in users:
            user['_id'] = str(user['_id'])
        return jsonify(users), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500