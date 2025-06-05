from flask import Blueprint, request, jsonify
from datetime import datetime
from database import get_db, generate_id
import json

shop_bp = Blueprint('shop', __name__)

def serialize_doc(row):
    doc = dict(row)
    if doc.get('categories'):
        doc['categories'] = json.loads(doc['categories'])
    return doc

@user_bp.route('/shops', methods=['POST'])
def create_shop():
    data = request.get_json()
    required_fields = ['name', 'owner', 'description', 'location']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT _id FROM users WHERE _id = ?', (data['owner'],))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'error': 'Owner user not found'}), 404
    
    shop_id = generate_id()
    created_at = datetime.utcnow().isoformat()
    shop_data = {
        '_id': shop_id,
        'name': data['name'],
        'owner': data['owner'],
        'description': data['description'],
        'logo': data.get('logo', ''),
        'location': data['location'],
        'categories': json.dumps(data.get('categories', [])),
        'isVerified': 1 if data.get('isVerified', False) else 0,
        'createdAt': created_at,
        'updatedAt': created_at
    }
    
    cursor.execute('''
        INSERT INTO shops (_id, name, owner, description, logo, location, categories, isVerified, createdAt, updatedAt)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        shop_data['_id'], shop_data['name'], shop_data['owner'], shop_data['description'],
        shop_data['logo'], shop_data['location'], shop_data['categories'], shop_data['isVerified'],
        shop_data['createdAt'], shop_data['updatedAt']
    ))
    
    conn.commit()
    conn.close()
    return jsonify({'_id': shop_id}), 201

@user_bp.route('/shops', methods=['GET'])
def get_all_shops():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM shops')
    shops = [serialize_doc(row) for row in cursor.fetchall()]
    
    for shop in shops:
        cursor.execute('SELECT * FROM shop_comments WHERE shop_id = ?', (shop['_id'],))
        shop['comments'] = [serialize_doc(row) for row in cursor.fetchall()]
    
    conn.close()
    return jsonify(shops), 200

@user_bp.route('/shops/<shop_id>', methods=['GET'])
def get_shop(shop_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM shops WHERE _id = ?', (shop_id,))
    shop = cursor.fetchone()
    
    if not shop:
        conn.close()
        return jsonify({'error': 'Shop not found'}), 404
    
    shop = serialize_doc(shop)
    cursor.execute('SELECT * FROM shop_comments WHERE shop_id = ?', (shop_id,))
    shop['comments'] = [serialize_doc(row) for row in cursor.fetchall()]
    
    conn.close()
    return jsonify(shop), 200

@user_bp.route('/shops/<shop_id>/comments', methods=['POST'])
def create_shop_comment(shop_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT _id FROM shops WHERE _id = ?', (shop_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'error': 'Shop not found'}), 404
    
    data = request.get_json()
    required_fields = ['user', 'comment']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    cursor.execute('SELECT _id FROM users WHERE _id = ?', (data['user'],))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'error': 'User not found'}), 404
    
    comment_id = generate_id()
    created_at = datetime.utcnow().isoformat()
    cursor.execute('''
        INSERT INTO shop_comments (_id, shop_id, user_id, comment, createdAt, updatedAt)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (comment_id, shop_id, data['user'], data['comment'], created_at, created_at))
    
    conn.commit()
    conn.close()
    return jsonify({'_id': comment_id}), 201