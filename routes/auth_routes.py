from flask import Blueprint, request, jsonify
from data_store import data_store, verify_password
import jwt
from datetime import datetime, timedelta
from functools import wraps

auth_bp = Blueprint('auth', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        try:
            token = token.split(" ")[1]  # Expect 'Bearer <token>'
            payload = jwt.decode(token, request.app.config['SECRET_KEY'], algorithms=['HS256'])
            request.user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email and password are required'}), 400
    
    user = next((u for u in data_store['users'].values() if u['email'] == data['email']), None)
    if not user or not verify_password(user['password'], data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    token = jwt.encode({
        'user_id': user['_id'],
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, request.app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({'token': token}), 200