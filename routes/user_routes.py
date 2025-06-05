from flask import Blueprint, request, jsonify
from datetime import datetime
from database import get_db, generate_id, hash_password
import json

user_bp = Blueprint('user', __name__)

def serialize_doc(row):
    return dict(row)

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    required_fields = ['name', 'email', 'password', 'address', 'phone']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT _id FROM users WHERE email = ?', (data['email'],))
    if cursor.fetchone():
        conn.close()
        return jsonify({'error': 'Email already exists'}), 400
    
    user_id = generate_id()
    created_at = datetime.utcnow().isoformat()
    user_data = {
        '_id': user_id,
        'name': data['name'],
        'email': data['email'],
        'password': hash_password(data['password']),
        'role': data.get('role', 'customer'),
        'address': data['address'],
        'phone': data['phone'],
        'profileImage': data.get('profileImage', ''),
        'createdAt': created_at,
        'updatedAt': created_at
    }
    
    cursor.execute('''
        INSERT INTO users (_id, name, email, password, role, address, phone, profileImage, createdAt, updatedAt)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_data['_id'], user_data['name'], user_data['email'], user_data['password'],
        user_data['role'], user_data['address'], user_data['phone'], user_data['profileImage'],
        user_data['createdAt'], user_data['updatedAt']
    ))
    
    conn.commit()
    conn.close()
    return jsonify({'_id': user_id}), 201

@user_bp.route('/users', methods=['GET'])
def get_all_users():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = [serialize_doc(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(users), 200

@user_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE _id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(serialize_doc(user)), 200

@user_bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT _id FROM users WHERE _id = ?', (user_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    update_data = {'updatedAt': datetime.utcnow().isoformat()}
    for field in ['name', 'email', 'address', 'phone', 'profileImage']:
        if field in data:
            update_data[field] = data[field]
    
    set_clause = ', '.join(f'{k} = ?' for k in update_data.keys())
    values = list(update_data.values()) + [user_id]
    
    cursor.execute(f'UPDATE users SET {set_clause} WHERE _id = ?', values)
    conn.commit()
    conn.close()
    return jsonify({'message': 'User updated'}), 200

@user_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT _id FROM users WHERE _id = ?', (user_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'error': 'User not found'}), 404
    
    cursor.execute('DELETE FROM users WHERE _id = ?', (user_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'User deleted'}), 200