from flask import Blueprint, request, jsonify
from .models import db, User

routes = Blueprint('routes', __name__)

@routes.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(
        name=data['name'],
        email=data['email'],
        password=data['password'] 
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@routes.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_data = [
        {
            'id': user.id,
            'name': user.name,
            'email': user.email
        }
        for user in users
    ]
    return jsonify(users_data), 200