from flask import jsonify, request, abort
from app import app, db  # Changed from config to app
from models import Proposal, ProposalStatusEnum

# CREATE
@app.route("/proposals", methods=["POST"])
def create_proposal():
    data = request.get_json()
    if not all(key in data for key in ["projectId", "freelancerId"]):
        abort(400, description="Missing required fields: projectId, freelancerId")
    try:
        new_proposal = Proposal(
            project_id=data["projectId"],
            freelancer_id=data["freelancerId"],
            cover_letter=data.get("coverLetter"),
            proposed_rate=data.get("proposedRate"),
            status=ProposalStatusEnum[data.get("status", "pending")]
        )
        db.session.add(new_proposal)
        db.session.commit()
        return jsonify({"message": "Proposal created", "proposal": new_proposal.to_json()}), 201
    except ValueError as e:
        abort(400, description=str(e))
    except Exception as e:
        db.session.rollback()
        abort(500, description="Failed to create proposal")

# READ ALL
@app.route("/proposals", methods=["GET"])
def get_proposals():
    proposals = Proposal.query.all()
    return jsonify({"proposals": [p.to_json() for p in proposals]})

# READ SINGLE
@app.route("/proposals/<int:id>", methods=["GET"])
def get_proposal(id):
    proposal = Proposal.query.get_or_404(id)
    return jsonify(proposal.to_json())

# UPDATE
@app.route("/proposals/<int:id>", methods=["PUT"])
def update_proposal(id):
    proposal = Proposal.query.get_or_404(id)
    data = request.get_json()
    proposal.cover_letter = data.get("coverLetter", proposal.cover_letter)
    proposal.proposed_rate = data.get("proposedRate", proposal.proposed_rate)
    proposal.status = ProposalStatusEnum[data.get("status", proposal.status.name)]
    db.session.commit()
    return jsonify({"message": "Proposal updated", "proposal": proposal.to_json()})

# DELETE
@app.route("/proposals/<int:id>", methods=["DELETE"])
def delete_proposal(id):
    proposal = Proposal.query.get_or_404(id)
    db.session.delete(proposal)
    db.session.commit()
    return jsonify({"message": "Proposal deleted"})