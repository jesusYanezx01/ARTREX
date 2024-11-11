from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import db, Category

category_routes = Blueprint('category_routes', __name__)

@category_routes.route('/categories', methods=['POST'])
@jwt_required()
def create_category():
    data = request.get_json()
    if not data.get('name'):
        return jsonify({"error": "The 'name' field is required"}), 400

    if Category.query.filter_by(name=data['name']).first():
        return jsonify({"error": "Category already exists"}), 400

    new_category = Category(
        name=data['name'],
        description=data.get('description', '')
    )
    db.session.add(new_category)
    db.session.commit()

    return jsonify({"message": "Category successfully created", "category": repr(new_category)}), 201

@category_routes.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    categories_data = [
        {
            'id': category.id,
            'name': category.name,
            'description': category.description,
            'created_at': category.created_at.isoformat()
        }
        for category in categories
    ]

    return jsonify(categories_data), 200

@category_routes.route('/categories/<int:category_id>', methods=['PUT'])
@jwt_required()
def update_category(category_id):
    data = request.get_json()
    category = Category.query.get(category_id)

    if not category:
        return jsonify({"error": "Category not found"}), 404

    category.name = data.get('name', category.name)
    category.description = data.get('description', category.description)
    db.session.commit()

    return jsonify({"message": "Category successfully updated", "category": repr(category)}), 200

@category_routes.route('/categories/<int:category_id>', methods=['DELETE'])
@jwt_required()
def delete_category(category_id):
    category = Category.query.get(category_id)

    if not category:
        return jsonify({"error": "Category not found"}), 404

    db.session.delete(category)
    db.session.commit()

    return jsonify({"message": "Category successfully deleted"}), 200