from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import db, Category, Level, LearningPath

learning_path_routes = Blueprint('learning_path_routes', __name__)

@learning_path_routes.route('/learning_paths', methods=['POST'])
@jwt_required()
def create_learning_path():
    data = request.get_json()

    if not data.get('title') or not data.get('category_id') or not data.get('level_id'):
        return jsonify({"error": "Fields 'title', 'category_id', and 'level_id' are required."}), 400

    category = Category.query.get(data['category_id'])
    level = Level.query.get(data['level_id'])

    if not category:
        return jsonify({"error": "Category does not exist."}), 404
    if not level:
        return jsonify({"error": "Level does not exist."}), 404

    new_learning_path = LearningPath(
        title=data['title'],
        description=data.get('description', ''),
        category_id=data['category_id'],
        level_id=data['level_id']
    )

    db.session.add(new_learning_path)
    db.session.commit()

    return jsonify({"message": "Learning path created successfully.", "learning_path": repr(new_learning_path)}), 201

@learning_path_routes.route('/learning_paths', methods=['GET'])
def get_learning_paths():
    category_id = request.args.get('category_id', type=int)
    level_id = request.args.get('level_id', type=int)
    title = request.args.get('title', type=str)

    query = LearningPath.query

    if category_id:
        query = query.filter_by(category_id=category_id)
    if level_id:
        query = query.filter_by(level_id=level_id)
    if title:
        query = query.filter(LearningPath.title.ilike(f'%{title}%'))

    learning_paths = query.all()

    learning_paths_data = [
        {
            'id': lp.id,
            'title': lp.title,
            'description': lp.description,
            'category_id': lp.category_id,
            'level_id': lp.level_id,
            'created_at': lp.created_at.isoformat()
        }
        for lp in learning_paths
    ]

    return jsonify(learning_paths_data), 200