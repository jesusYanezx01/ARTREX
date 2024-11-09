from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Score, LearningPath

score_routes = Blueprint('score_routes', __name__)

@score_routes.route('/scores', methods=['POST'])
@jwt_required()
def add_or_update_score():
    data = request.get_json()
    user_id = get_jwt_identity()['id']

    if not data.get('value') or not data.get('learning_path_id'):
        return jsonify({"error": "The fields 'value' and 'learning_path_id' are required"}), 400

    if data['value'] < 1 or data['value'] > 5:
        return jsonify({"error": "The score must be between 1 and 5"}), 400

    learning_path = LearningPath.query.get(data['learning_path_id'])
    if not learning_path:
        return jsonify({"error": "The learning path does not exist"}), 404

    score = Score.query.filter_by(user_id=user_id, learning_path_id=data['learning_path_id']).first()

    if score:
        score.value = data['value']
        message = "Score successfully updated"
    else:
        score = Score(
            value=data['value'],
            user_id=user_id,
            learning_path_id=data['learning_path_id']
        )
        db.session.add(score)
        message = "Score successfully added"

    db.session.commit()

    return jsonify({"message": message, "score": repr(score)}), 201

@score_routes.route('/scores/<int:learning_path_id>', methods=['GET'])
def get_scores(learning_path_id):
    scores = Score.query.filter_by(learning_path_id=learning_path_id).all()
    if not scores:
        return jsonify({"message": "No scores for this learning path"}), 404

    scores_data = [
        {
            'id': score.id,
            'value': score.value,
            'user_id': score.user_id,
            'created_at': score.created_at.isoformat()
        }
        for score in scores
    ]

    average_score = sum([score.value for score in scores]) / len(scores)

    return jsonify({"scores": scores_data, "average_score": round(average_score, 2)}), 200

@score_routes.route('/scores/<int:score_id>', methods=['DELETE'])
@jwt_required()
def delete_score(score_id):
    user_id = get_jwt_identity()['id']

    score = Score.query.get(score_id)
    if not score:
        return jsonify({"error": "The score does not exist"}), 404

    if score.user_id != user_id:
        return jsonify({"error": "You do not have permission to delete this score"}), 403

    db.session.delete(score)
    db.session.commit()

    return jsonify({"message": "Score successfully deleted"}), 200