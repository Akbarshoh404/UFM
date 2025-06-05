from flask import Blueprint, request, jsonify
from bson import ObjectId
from datetime import datetime
from config import db

order_bp = Blueprint('order', __name__)
orders = db['orders']

def serialize_doc(doc):
    if isinstance(doc, list):
        return [serialize_doc(item) for item in doc]
    if isinstance(doc, dict):
        return {k: str(v) if isinstance(v, ObjectId) else v for k, v in doc.items()}
    return doc

@order_bp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    required_fields = ['user', 'products', 'deliveryAddress', 'totalPrice']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    order_data = {
        'user': ObjectId(data['user']),
        'products': [{'product': ObjectId(p['product']), 'quantity': p['quantity']} for p in data['products']],
        'deliveryAddress': data['deliveryAddress'],
        'status': data.get('status', 'pending'),
        'totalPrice': data['totalPrice'],
        'paymentStatus': data.get('paymentStatus', 'pending'),
        'createdAt': datetime.utcnow(),
        'updatedAt': datetime.utcnow()
    }
    result = orders.insert_one(order_data)
    return jsonify({'_id': str(result.inserted_id)}), 201

@order_bp.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    order = orders.find_one({'_id': ObjectId(order_id)})
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    return jsonify(serialize_doc(order)), 200