from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from routes import register_routes

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/fashion_market"
CORS(app)

mongo = PyMongo(app)
register_routes(app, mongo)

if __name__ == "__main__":
    app.run(debug=True)
