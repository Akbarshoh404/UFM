from flask import Blueprint, jsonify, request, abort
from app import db
from models import Contract, ContractStatusEnum

contract_bp = Blueprint('contract', __name__, url_prefix='/contracts')

# CREATE
@contract_bp.route("/", methods=["POST"])
def create_contract():
    data = request.get_json()
    if not all(key in data for key in ["proposalId", "clientId", "freelancerId"]):
        abort(400, description="Missing required fields: proposalId, clientId, freelancerId")
    try:
        new_contract = Contract(
            project_id=data["proposalId"],
            client_id=data["clientId"],
            freelancer_id=data["freelancerId"],
            terms=data.get("terms"),
            agreed_rate=data.get("totalAmount"),
            status=ContractStatusEnum[data.get("status", "active")]
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
@contract_bp.route("/", methods=["GET"])
def get_contracts():
    contracts = Contract.query.all()
    return jsonify({"contracts": [c.to_json() for c in contracts]})

# READ SINGLE
@contract_bp.route("/<int:id>", methods=["GET"])
def get_contract(id):
    contract = Contract.query.get_or_404(id)
    return jsonify(contract.to_json())

# UPDATE
@contract_bp.route("/<int:id>", methods=["PUT"])
def update_contract(id):
    contract = Contract.query.get_or_404(id)
    data = request.get_json()
    contract.terms = data.get("terms", contract.terms)
    contract.agreed_rate = data.get("totalAmount", contract.agreed_rate)
    contract.status = ContractStatusEnum[data.get("status", contract.status.name)]
    db.session.commit()
    return jsonify({"message": "Contract updated", "contract": contract.to_json()})

# DELETE
@contract_bp.route("/<int:id>", methods=["DELETE"])
def delete_contract(id):
    contract = Contract.query.get_or_404(id)
    db.session.delete(contract)
    db.session.commit()
    return jsonify({"message": "Contract deleted"})