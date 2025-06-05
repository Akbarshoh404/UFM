from flask import Blueprint, request, jsonify
from database import get_db, generate_id
from datetime import datetime

shop_bp = Blueprint('shop', __name__)

@shop_bp.route('/shops', methods=['POST'])
def create_shop():
    try:
        data = request.get_json()
        db = get_db()
        cursor = db.cursor()
        
        shop_id = generate_id()
        created_at = datetime.utcnow().isoformat()
        updated_at = created_at
        
        cursor.execute('''
            INSERT INTO shops (_id, name, owner, description, logo, location, categories, isVerified, createdAt, updatedAt)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            shop_id,
            data['name'],
            data['owner'],
            data['description'],
            data.get('logo', ''),
            data['location'],
            data.get('categories', ''),
            0,
            created_at,
            updated_at
        ))
        
        db.commit()
        return jsonify({'_id': shop_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@shop_bp.route('/shops', methods=['GET'])
def get_shops():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM shops')
        shops = [dict(row) for row in cursor.fetchall()]
        return jsonify(shops), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()