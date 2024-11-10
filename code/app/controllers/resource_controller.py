from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import db, Resource, LearningPath

resource_routes = Blueprint('resource_routes', __name__)

@resource_routes.route('/resources', methods=['POST'])
@jwt_required()
def add_resource():
    data = request.get_json()

    if not data.get('title') or not data.get('url') or not data.get('learning_path_id'):
        return jsonify({"error": "Fields 'title', 'url', and 'learning_path_id' are required"}), 400

    learning_path = LearningPath.query.get(data['learning_path_id'])
    if not learning_path:
        return jsonify({"error": "Learning path does not exist"}), 404

    new_resource = Resource(
        title=data['title'],
        url=data['url'],
        description=data.get('description', ''),
        learning_path_id=data['learning_path_id']
    )
    db.session.add(new_resource)
    db.session.commit()

    return jsonify({"message": "Resource added successfully", "resource": repr(new_resource)}), 201

@resource_routes.route('/resources/<int:learning_path_id>', methods=['GET'])
def get_resources(learning_path_id):
    resources = Resource.query.filter_by(learning_path_id=learning_path_id).all()
    if not resources:
        return jsonify({"message": "No resources found for this learning path"}), 404

    resources_data = [
        {
            'id': resource.id,
            'title': resource.title,
            'url': resource.url,
            'description': resource.description,
            'created_at': resource.created_at.isoformat()
        }
        for resource in resources
    ]

    return jsonify(resources_data), 200

@resource_routes.route('/resources/<int:resource_id>', methods=['PUT'])
@jwt_required()
def update_resource(resource_id):
    data = request.get_json()
    resource = Resource.query.get(resource_id)

    if not resource:
        return jsonify({"error": "Resource does not exist"}), 404

    resource.title = data.get('title', resource.title)
    resource.url = data.get('url', resource.url)
    resource.description = data.get('description', resource.description)
    db.session.commit()

    return jsonify({"message": "Resource updated successfully", "resource": repr(resource)}), 200

# Endpoint para eliminar un recurso específico
@resource_routes.route('/resources/<int:resource_id>', methods=['DELETE'])
@jwt_required()
def delete_resource(resource_id):
    resource = Resource.query.get(resource_id)

    if not resource:
        return jsonify({"error": "Resource does not exist"}), 404

    db.session.delete(resource)
    db.session.commit()

    return jsonify({"message": "Resource deleted successfully"}), 200