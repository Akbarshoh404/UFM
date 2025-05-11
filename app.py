from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Import blueprints
from routes.user_routes import user_bp
from routes.project_routes import project_bp
from routes.proposal_routes import proposal_bp
from routes.contract_routes import contract_bp
from routes.payment_routes import payment_bp
from routes.message_routes import message_bp
from routes.admin_routes import admin_bp

# Register blueprints
app.register_blueprint(user_bp)
app.register_blueprint(project_bp)
app.register_blueprint(proposal_bp)
app.register_blueprint(contract_bp)
app.register_blueprint(payment_bp)
app.register_blueprint(message_bp)
app.register_blueprint(admin_bp)

# Create database tables before the first request
with app.app_context():
    db.create_all()

# Debug route to list all registered routes
@app.route('/routes')
def list_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': list(rule.methods),
            'rule': str(rule)
        })
    return jsonify({'routes': routes})

# Global error handler for 500 errors
@app.errorhandler(Exception)
def handle_error(error):
    app.logger.error(f"Unhandled error: {str(error)}")
    response = jsonify({"error": "Internal Server Error", "message": str(error)})
    response.status_code = 500
    return response

# Error handler for SQLAlchemy errors
@app.errorhandler(SQLAlchemyError)
def handle_sqlalchemy_error(error):
    app.logger.error(f"Database error: {str(error)}")
    response = jsonify({"error": "Database Error", "message": str(error)})
    response.status_code = 500
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))