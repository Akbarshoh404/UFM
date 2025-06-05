from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['uzbekistan_fashion_market']