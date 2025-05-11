from flask import Blueprint, jsonify, request
from app import db
from models import Message

message_bp = Blueprint('message', __name__, url_prefix='/messages')

# CREATE
@message_bp.route("/", methods=["POST"])
def create_message():
    data = request.get_json()
    new_message = Message(
        sender_id=data["senderId"],
        receiver_id=data["receiverId"],
        text=data["text"]
    )
    db.session.add(new_message)
    db.session.commit()
    return jsonify({"message": "Message created", "message": new_message.to_json()}), 201

# READ ALL
@message_bp.route("/", methods=["GET"])
def get_messages():
    messages = Message.query.all()
    return jsonify({"messages": [m.to_json() for m in messages]})

# READ SINGLE
@message_bp.route("/<int:id>", methods=["GET"])
def get_message(id):
    message = Message.query.get_or_404(id)
    return jsonify(message.to_json())

# DELETE
@message_bp.route("/<int:id>", methods=["DELETE"])
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return jsonify({"message": "Message deleted"})