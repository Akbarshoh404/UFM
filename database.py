import sqlite3
import uuid
import bcrypt
from datetime import datetime
import os

DB_PATH = '/tmp/uzbekistan_fashion_market.db'

def init_db():
    try:
        # Ensure /tmp directory is writable
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                _id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'customer',
                address TEXT NOT NULL,
                phone TEXT NOT NULL,
                profileImage TEXT,
                createdAt TEXT NOT NULL,
                updatedAt TEXT NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shops (
                _id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                owner TEXT NOT NULL,
                description TEXT NOT NULL,
                logo TEXT,
                location TEXT NOT NULL,
                categories TEXT,
                isVerified INTEGER DEFAULT 0,
                createdAt TEXT NOT NULL,
                updatedAt TEXT NOT NULL,
                FOREIGN KEY (owner) REFERENCES users(_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shop_comments (
                _id TEXT PRIMARY KEY,
                shop_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                comment TEXT NOT NULL,
                createdAt TEXT NOT NULL,
                updatedAt TEXT NOT NULL,
                FOREIGN KEY (shop_id) REFERENCES shops(_id),
                FOREIGN KEY (user_id) REFERENCES users(_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                _id TEXT PRIMARY KEY,
                shop_id TEXT NOT NULL,
                name TEXT NOT NULL,
                images TEXT,
                price REAL NOT NULL,
                description TEXT NOT NULL,
                size TEXT,
                color TEXT,
                stock INTEGER DEFAULT 0,
                category TEXT NOT NULL,
                ratingsAverage REAL DEFAULT 0.0,
                createdAt TEXT NOT NULL,
                updatedAt TEXT NOT NULL,
                FOREIGN KEY (shop_id) REFERENCES shops(_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_reviews (
                _id TEXT PRIMARY KEY,
                product_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                rating INTEGER NOT NULL,
                comment TEXT NOT NULL,
                createdAt TEXT NOT NULL,
                updatedAt TEXT NOT NULL,
                FOREIGN KEY (product_id) REFERENCES products(_id),
                FOREIGN KEY (user_id) REFERENCES users(_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                _id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                products TEXT NOT NULL,
                deliveryAddress TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                totalPrice REAL NOT NULL,
                paymentStatus TEXT DEFAULT 'pending',
                createdAt TEXT NOT NULL,
                updatedAt TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(_id)
            )
        ''')
        
        conn.commit()
    except Exception as e:
        print(f"Database initialization error: {e}")
        raise
    finally:
        conn.close()

def generate_id():
    return str(uuid.uuid4())

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database on module load
try:
    init_db()
except Exception as e:
    print(f"Failed to initialize database: {e}")