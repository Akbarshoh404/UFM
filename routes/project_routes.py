from flask import Blueprint, jsonify, request, abort
from app import db
from models import Project, ProjectStatusEnum

project_bp = Blueprint('project', __name__, url_prefix='/projects')

# CREATE
@project_bp.route("/", methods=["POST"])
def create_project():
    data = request.get_json()
    if not all(key in data for key in ["title", "clientId"]):
        abort(400, description="Missing required fields: title, clientId")
    try:
        new_project = Project(
            title=data["title"],
            description=data.get("description"),
            category=data.get("category"),
            budget=data.get("budget"),
            duration=data.get("duration"),
            client_id=data["clientId"],
            status=ProjectStatusEnum[data.get("status", "open")]
        )
        db.session.add(new_project)
        db.session.commit()
        return jsonify({"message": "Project created", "project": new_project.to_json()}), 201
    except ValueError as e:
        abort(400, description=str(e))
    except Exception as e:
        db.session.rollback()
        abort(500, description="Failed to create project")

# READ ALL
@project_bp.route("/", methods=["GET"])
def get_projects():
    projects = Project.query.all()
    return jsonify({"projects": [p.to_json() for p in projects]})

# READ SINGLE
@project_bp.route("/<int:id>", methods=["GET"])
def get_project(id):
    project = Project.query.get_or_404(id)
    return jsonify(project.to_json())

# UPDATE
@project_bp.route("/<int:id>", methods=["PUT"])
def update_project(id):
    project = Project.query.get_or_404(id)
    data = request.get_json()
    project.title = data.get("title", project.title)
    project.description = data.get("description", project.description)
    project.category = data.get("category", project.category)
    project.budget = data.get("budget", project.budget)
    project.duration = data.get("duration", project.duration)
    project.status = ProjectStatusEnum[data.get("status", project.status.name)]
    db.session.commit()
    return jsonify({"message": "Project updated", "project": project.to_json()})

# DELETE
@project_bp.route("/<int:id>", methods=["DELETE"])
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return jsonify({"message": "Project deleted"})