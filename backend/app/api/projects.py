from flask import jsonify
from backend.app import db
from . import api
from .errors import forbidden
from backend.app.models.projects import Projects


@api.route('/projects')
def get_groups():
    projects = Projects.objects()
    return jsonify({
        'projects': [project.to_json() for project in projects],
    })


@api.route('/projects/<string:id>')
def get_project():
    project = Projects.objects.get_or_404(id=id)
    return jsonify(project.to_json())
