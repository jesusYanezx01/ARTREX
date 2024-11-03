from flask import Blueprint, jsonify
from app.models import Level

level_routes = Blueprint('level_routes', __name__)

@level_routes.route('/levels', methods=['GET'])
def get_levels():
    levels = Level.query.all()
    levels_data = [
        {
            'id': level.id,
            'name': level.name,
            'description': level.description,
            'created_at': level.created_at
        }
        for level in levels
    ]
    return jsonify(levels_data), 200