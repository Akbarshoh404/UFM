from flask import Blueprint, request, jsonify
from datetime import datetime
from database import get_db, generate_id
import json

order_bp = Blueprint('order', __name__)

def serialize_doc(row):
    doc = dict(row)
    doc['products'] = json.loads(doc['products'])
    return doc

@order_bp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    required_fields = ['user', 'products', 'deliveryAddress', 'totalPrice']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT _id FROM users WHERE _id = ?', (data['user'],))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'error': 'User not found'}), 404
    
    for p in data['products']:
        cursor.execute('SELECT _id FROM products WHERE _id = ?', (p['product'],))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'error': f"Product {p['product']} not found"}), 404
    
    order_id = generate_id()
    created_at = datetime.utcnow().isoformat()
    order_data = {
        '_id': order_id,
        'user_id': data['user'],
        'products': json.dumps(data['products']),
        'deliveryAddress': data['deliveryAddress'],
        'status': data.get('status', 'pending'),
        'totalPrice': data['totalPrice'],
        'paymentStatus': data.get('paymentStatus', 'pending'),
        'createdAt': created_at,
        'updatedAt': created_at
    }
    
    cursor.execute('''
        INSERT INTO orders (_id, user_id, products, deliveryAddress, status, totalPrice, paymentStatus, createdAt, updatedAt)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        order_data['_id'], order_data['user_id'], order_data['products'], order_data['deliveryAddress'],
        order_data['status'], order_data['totalPrice'], order_data['paymentStatus'],
        order_data['createdAt'], order_data['updatedAt']
    ))
    
    conn.commit()
    conn.close()
    return jsonify({'_id': order_id}), 201

@order_bp.route('/orders', methods=['GET'])
def get_all_orders():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders')
    orders = [serialize_doc(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(orders), 200

@order_bp.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders WHERE _id = ?', (order_id,))
    order = cursor.fetchone()
    conn.close()
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    return jsonify(serialize_doc(order)), 200