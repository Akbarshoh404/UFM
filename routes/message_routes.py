from flask import jsonify, request
from config import app, db
from models import Message

# CREATE
@app.route("/messages", methods=["POST"])
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
@app.route("/messages", methods=["GET"])
def get_messages():
    messages = Message.query.all()
    return jsonify({"messages": [m.to_json() for m in messages]})

# READ SINGLE
@app.route("/messages/<int:id>", methods=["GET"])
def get_message(id):
    message = Message.query.get_or_404(id)
    return jsonify(message.to_json())

# DELETE
@app.route("/messages/<int:id>", methods=["DELETE"])
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return jsonify({"message": "Message deleted"})