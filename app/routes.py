from flask import Blueprint, jsonify

api = Blueprint('api', __name__)

@api.route('/hello', methods=['GET'])
def hello_world():
    return jsonify(message="¡Hola, Mundo!")