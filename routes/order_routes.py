from flask import Blueprint, request, jsonify
from datetime import datetime
from data_store import data_store, generate_id

order_bp = Blueprint('order', __name__)

def serialize_doc(doc):
    return doc

@order_bp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    required_fields = ['user', 'products', 'deliveryAddress', 'totalPrice']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    order_id = generate_id()
    order_data = {
        '_id': order_id,
        'user': data['user'],
        'products': data['products'],  # List of {product, quantity}
        'deliveryAddress': data['deliveryAddress'],
        'status': data.get('status', 'pending'),
        'totalPrice': data['totalPrice'],
        'paymentStatus': data.get('paymentStatus', 'pending'),
        'createdAt': datetime.utcnow().isoformat(),
        'updatedAt': datetime.utcnow().isoformat()
    }
    data_store['orders'][order_id] = order_data
    return jsonify({'_id': order_id}), 201

@order_bp.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    order = data_store['orders'].get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    return jsonify(serialize_doc(order)), 200