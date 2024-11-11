from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import db, Label, LearningPath

label_routes = Blueprint('label_routes', __name__)

@label_routes.route('/labels', methods=['POST'])
@jwt_required()
def assign_label():
    data = request.get_json()
    if not data.get('name') or not data.get('learning_path_id'):
        return jsonify({"error": "The 'name' and 'learning_path_id' fields are required"}), 400

    learning_path = LearningPath.query.get(data['learning_path_id'])
    if not learning_path:
        return jsonify({"error": "Learning path does not exist"}), 404

    label = Label.query.filter_by(name=data['name']).first()
    if not label:
        label = Label(name=data['name'], description=data.get('description', ''))
        db.session.add(label)
        db.session.commit()

    if label not in learning_path.labels:
        learning_path.labels.append(label)
        db.session.commit()
        return jsonify({"message": "Label assigned successfully", "label": repr(label)}), 201
    else:
        return jsonify({"message": "Label is already assigned to this learning path"}), 200

@label_routes.route('/labels/<int:learning_path_id>', methods=['GET'])
def get_labels(learning_path_id):
    learning_path = LearningPath.query.get(learning_path_id)
    if not learning_path:
        return jsonify({"error": "Learning path does not exist"}), 404

    labels_data = [
        {
            'id': label.id,
            'name': label.name,
            'description': label.description,
            'created_at': label.created_at.isoformat()
        }
        for label in learning_path.labels
    ]

    return jsonify(labels_data), 200

@label_routes.route('/labels/<int:learning_path_id>/<int:label_id>', methods=['DELETE'])
@jwt_required()
def delete_label_from_learning_path(learning_path_id, label_id):
    learning_path = LearningPath.query.get(learning_path_id)
    label = Label.query.get(label_id)

    if not learning_path or not label:
        return jsonify({"error": "Learning path or label does not exist"}), 404

    if label in learning_path.labels:
        learning_path.labels.remove(label)
        db.session.commit()
        return jsonify({"message": "Label removed successfully"}), 200
    else:
        return jsonify({"error": "Label is not assigned to this learning path"}), 404
