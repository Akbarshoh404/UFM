from flask import jsonify, request
from config import app, db
from models import Contract, ContractStatusEnum

# CREATE
@app.route("/contracts", methods=["POST"])
def create_contract():
    data = request.get_json()
    new_contract = Contract(
        project_id=data["projectId"],
        client_id=data["clientId"],
        freelancer_id=data["freelancerId"],
        agreed_rate=data["agreedRate"],
        status=ContractStatusEnum[data.get("status", "active")]
    )
    db.session.add(new_contract)
    db.session.commit()
    return jsonify({"message": "Contract created", "contract": new_contract.to_json()}), 201

# READ ALL
@app.route("/contracts", methods=["GET"])
def get_contracts():
    contracts = Contract.query.all()
    return jsonify({"contracts": [c.to_json() for c in contracts]})

# READ SINGLE
@app.route("/contracts/<int:id>", methods=["GET"])
def get_contract(id):
    contract = Contract.query.get_or_404(id)
    return jsonify(contract.to_json())

# UPDATE
@app.route("/contracts/<int:id>", methods=["PUT"])
def update_contract(id):
    contract = Contract.query.get_or_404(id)
    data = request.get_json()
    contract.agreed_rate = data.get("agreedRate", contract.agreed_rate)
    contract.status = ContractStatusEnum[data.get("status", contract.status.name)]
    contract.ended_at = data.get("endedAt", contract.ended_at)
    db.session.commit()
    return jsonify({"message": "Contract updated", "contract": contract.to_json()})

# DELETE
@app.route("/contracts/<int:id>", methods=["DELETE"])
def delete_contract(id):
    contract = Contract.query.get_or_404(id)
    db.session.delete(contract)
    db.session.commit()
    return jsonify({"message": "Contract deleted"})