import os
from pymongo import MongoClient
import uuid
from bcrypt import hashpw, gensalt
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

def get_mongo_client():
    """Initialize and return MongoDB client."""
    try:
        mongo_uri = os.getenv('MONGODB_URI')
        if not mongo_uri:
            raise ValueError("MONGODB_URI environment variable not set")
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        client.server_info()  # Test connection
        return client
    except Exception as e:
        raise Exception(f"Failed to connect to MongoDB: {str(e)}")

def get_db():
    """Return the database instance."""
    client = get_mongo_client()
    return client['uzbekistan_fashion_market']

def generate_id():
    """Generate a unique ID for documents."""
    return str(uuid.uuid4())

def hash_password(password):
    """Hash a password using bcrypt."""
    return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')