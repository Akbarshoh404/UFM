from flask import jsonify, request
from app import app, db
from models import Admin
from werkzeug.security import generate_password_hash

# CREATE
@app.route("/admins", methods=["POST"])
def create_admin():
    data = request.get_json()
    new_admin = Admin(
        email=data["email"],
        password=generate_password_hash(data["password"]),  # Hash the password
        permissions=data.get("permissions", [])
    )
    db.session.add(new_admin)
    db.session.commit()
    return jsonify({"message": "Admin created", "admin": new_admin.to_json()}), 201

# READ ALL
@app.route("/admins", methods=["GET"])
def get_admins():
    admins = Admin.query.all()
    return jsonify({"admins": [a.to_json() for a in admins]})

# READ SINGLE
@app.route("/admins/<int:id>", methods=["GET"])
def get_admin(id):
    admin = Admin.query.get_or_404(id)
    return jsonify(admin.to_json())

# UPDATE
@app.route("/admins/<int:id>", methods=["PUT"])
def update_admin(id):
    admin = Admin.query.get_or_404(id)
    data = request.get_json()
    admin.email = data.get("email", admin.email)
    admin.password = data.get("password", admin.password)  # Note: Hash password in production
    admin.permissions = data.get("permissions", admin.permissions)
    db.session.commit()
    return jsonify({"message": "Admin updated", "admin": admin.to_json()})

# DELETE
@app.route("/admins/<int:id>", methods=["DELETE"])
def delete_admin(id):
    admin = Admin.query.get_or_404(id)
    db.session.delete(admin)
    db.session.commit()
    return jsonify({"message": "Admin deleted"})