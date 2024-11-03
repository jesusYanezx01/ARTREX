from flask import Blueprint, jsonify
from app.models import Category

category_routes = Blueprint('category_routes', __name__)

@category_routes.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    categories_data = [
        {
            'id': category.id,
            'name': category.name,
            'description': category.description,
            'created_at': category.created_at
        }
        for category in categories
    ]
    return jsonify(categories_data), 200