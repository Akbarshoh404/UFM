from flask import jsonify, request, abort
from app import app, db  # Changed from config to app
from models import Contract, ContractStatusEnum

# CREATE
@app.route("/contracts", methods=["POST"])
def create_contract():
    data = request.get_json()
    if not all(key in data for key in ["proposalId", "clientId", "freelancerId"]):
        abort(400, description="Missing required fields: proposalId, clientId, freelancerId")
    try:
        new_contract = Contract(
            proposal_id=data["proposalId"],
            client_id=data["clientId"],
            freelancer_id=data["freelancerId"],
            terms=data.get("terms"),
            total_amount=data.get("totalAmount"),
            status=ContractStatusEnum[data.get("status", "pending")]
        )
        db.session.add(new_contract)
        db.session.commit()
        return jsonify({"message": "Contract created", "contract": new_contract.to_json()}), 201
    except ValueError as e:
        abort(400, description=str(e))
    except Exception as e:
        db.session.rollback()
        abort(500, description="Failed to create contract")

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
    contract.terms = data.get("terms", contract.terms)
    contract.total_amount = data.get("totalAmount", contract.total_amount)
    contract.status = ContractStatusEnum[data.get("status", contract.status.name)]
    db.session.commit()
    return jsonify({"message": "Contract updated", "contract": contract.to_json()})

# DELETE
@app.route("/contracts/<int:id>", methods=["DELETE"])
def delete_contract(id):
    contract = Contract.query.get_or_404(id)
    db.session.delete(contract)
    db.session.commit()
    return jsonify({"message": "Contract deleted"})