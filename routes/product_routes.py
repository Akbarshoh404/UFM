from flask import Blueprint, request, jsonify
from datetime import datetime
from database import get_db, generate_id
import json

product_bp = Blueprint('product', __name__)

def serialize_doc(row):
    doc = dict(row)
    if doc.get('images'):
        doc['images'] = json.loads(doc['images'])
    if doc.get('size'):
        doc['size'] = json.loads(doc['size'])
    if doc.get('color'):
        doc['color'] = json.loads(doc['color'])
    return doc

@product_bp.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    required_fields = ['shop', 'name', 'price', 'description', 'category']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT _id FROM shops WHERE _id = ?', (data['shop'],))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'error': 'Shop not found'}), 404
    
    product_id = generate_id()
    created_at = datetime.utcnow().isoformat()
    product_data = {
        '_id': product_id,
        'shop_id': data['shop'],
        'name': data['name'],
        'images': json.dumps(data.get('images', [])),
        'price': data['price'],
        'description': data['description'],
        'size': json.dumps(data.get('size', [])),
        'color': json.dumps(data.get('color', [])),
        'stock': data.get('stock', 0),
        'category': data['category'],
        'ratingsAverage': data.get('ratingsAverage', 0.0),
        'createdAt': created_at,
        'updatedAt': created_at
    }
    
    cursor.execute('''
        INSERT INTO products (_id, shop_id, name, images, price, description, size, color, stock, category, ratingsAverage, createdAt, updatedAt)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        product_data['_id'], product_data['shop_id'], product_data['name'], product_data['images'],
        product_data['price'], product_data['description'], product_data['size'], product_data['color'],
        product_data['stock'], product_data['category'], product_data['ratingsAverage'],
        product_data['createdAt'], product_data['updatedAt']
    ))
    
    conn.commit()
    conn.close()
    return jsonify({'_id': product_id}), 201

@product_bp.route('/products', methods=['GET'])
def get_all_products():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = [serialize_doc(row) for row in cursor.fetchall()]
    
    for product in products:
        cursor.execute('SELECT * FROM product_reviews WHERE product_id = ?', (product['_id'],))
        product['reviews'] = [serialize_doc(row) for row in cursor.fetchall()]
    
    conn.close()
    return jsonify(products), 200

@product_bp.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE _id = ?', (product_id,))
    product = cursor.fetchone()
    
    if not product:
        conn.close()
        return jsonify({'error': 'Product not found'}), 404
    
    product = serialize_doc(product)
    cursor.execute('SELECT * FROM product_reviews WHERE product_id = ?', (product_id,))
    product['reviews'] = [serialize_doc(row) for row in cursor.fetchall()]
    
    conn.close()
    return jsonify(product), 200

@product_bp.route('/products/<product_id>/reviews', methods=['POST'])
def create_product_review(product_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT _id FROM products WHERE _id = ?', (product_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'error': 'Product not found'}), 404
    
    data = request.get_json()
    required_fields = ['user', 'rating', 'comment']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    cursor.execute('SELECT _id FROM users WHERE _id = ?', (data['user'],))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'error': 'User not found'}), 404
    
    review_id = generate_id()
    created_at = datetime.utcnow().isoformat()
    cursor.execute('''
        INSERT INTO product_reviews (_id, product_id, user_id, rating, comment, createdAt, updatedAt)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (review_id, product_id, data['user'], data['rating'], data['comment'], created_at, created_at))
    
    # Update ratingsAverage
    cursor.execute('SELECT rating FROM product_reviews WHERE product_id = ?', (product_id,))
    ratings = [row['rating'] for row in cursor.fetchall()]
    ratings_average = sum(ratings) / len(ratings) if ratings else 0.0
    cursor.execute('UPDATE products SET ratingsAverage = ? WHERE _id = ?', (ratings_average, product_id))
    
    conn.commit()
    conn.close()
    return jsonify({'_id': review_id}), 201