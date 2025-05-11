from flask import Blueprint, jsonify, request
from app import db
from models import Admin
from werkzeug.security import generate_password_hash

admin_bp = Blueprint('admin', __name__, url_prefix='/admins')

# CREATE
@admin_bp.route("/", methods=["POST"])
def create_admin():
    data = request.get_json()
    new_admin = Admin(
        email=data["email"],
        password=generate_password_hash(data["password"]),
        permissions=data.get("permissions", [])
    )
    db.session.add(new_admin)
    db.session.commit()
    return jsonify({"message": "Admin created", "admin": new_admin.to_json()}), 201

# READ ALL
@admin_bp.route("/", methods=["GET"])
def get_admins():
    admins = Admin.query.all()
    return jsonify({"admins": [a.to_json() for a in admins]})

# READ SINGLE
@admin_bp.route("/<int:id>", methods=["GET"])
def get_admin(id):
    admin = Admin.query.get_or_404(id)
    return jsonify(admin.to_json())

# UPDATE
@admin_bp.route("/<int:id>", methods=["PUT"])
def update_admin(id):
    admin = Admin.query.get_or_404(id)
    data = request.get_json()
    admin.email = data.get("email", admin.email)
    if "password" in data:
        admin.password = generate_password_hash(data["password"])
    admin  # Hash password
    admin.permissions = data.get("permissions", admin.permissions)
    db.session.commit()
    return jsonify({"message": "Admin updated", "admin": admin.to_json()})

# DELETE
@admin_bp.route("/<int:id>", methods=["DELETE"])
def delete_admin(id):
    admin = Admin.query.get_or_404(id)
    db.session.delete(admin)
    db.session.commit()
    return jsonify({"message": "Admin deleted"})