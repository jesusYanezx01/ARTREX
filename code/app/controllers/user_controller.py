from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import db, User

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/users', methods=['POST'])
def create_user():
    data = request.json
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'message': 'Email already exists'}), 400
    
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        role=data['role']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@user_routes.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    try:
        users = User.query.all()
        users_data = [
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role
            }
            for user in users
        ]
        return jsonify(users_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500