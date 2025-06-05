from datetime import datetime
import uuid
import bcrypt

# In-memory data store
data_store = {
    'users': {},
    'shops': {},
    'products': {},
    'orders': {},
    'product_reviews': {},
    'shop_comments': {}
}

def generate_id():
    return str(uuid.uuid4())

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')