from flask import Flask, jsonify, request
from config import app, db
from models import User, RoleEnum

# CREATE
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = User(
        name=data["name"],
        email=data["email"],
        password=data["password"],  # Note: In production, hash the password
        role=RoleEnum[data.get("role", "freelancer")]
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created", "user": new_user.to_json()}), 201

# READ ALL
@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    json_users = [u.to_json() for u in users]
    return jsonify({"users": json_users})

# READ SINGLE
@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())

# UPDATE FULL (PUT)
@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    user.name = data.get("name", user.name)
    user.email = data.get("email", user.email)
    user.password = data.get("password", user.password)  # Note: Hash password in production
    user.role = RoleEnum[data.get("role", user.role.name)] if "role" in data else user.role
    db.session.commit()
    return jsonify({"message": "User updated", "user": user.to_json()})

# PARTIAL UPDATE (PATCH)
@app.route("/users/<int:id>", methods=["PATCH"])
def patch_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    
    if "name" in data:
        user.name = data["name"]
    if "email" in data:
        user.email = data["email"]
    if "password" in data:
        user.password = data["password"]  # Note: Hash password in production
    if "role" in data:
        user.role = RoleEnum[data["role"]]

    db.session.commit()
    return jsonify({"message": "User partially updated", "user": user.to_json()})

# DELETE
@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"})

# App Runner
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)