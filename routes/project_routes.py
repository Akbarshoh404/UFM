from flask import jsonify, request
from config import app, db
from models import Project, ProjectStatusEnum

# CREATE
@app.route("/projects", methods=["POST"])
def create_project():
    data = request.get_json()
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

# READ ALL
@app.route("/projects", methods=["GET"])
def get_projects():
    projects = Project.query.all()
    return jsonify({"projects": [p.to_json() for p in projects]})

# READ SINGLE
@app.route("/projects/<int:id>", methods=["GET"])
def get_project(id):
    project = Project.query.get_or_404(id)
    return jsonify(project.to_json())

# UPDATE
@app.route("/projects/<int:id>", methods=["PUT"])
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
@app.route("/projects/<int:id>", methods=["DELETE"])
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return jsonify({"message": "Project deleted"})