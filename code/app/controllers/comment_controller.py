from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Comment, LearningPath

comment_routes = Blueprint('comment_routes', __name__)

@comment_routes.route('/comments', methods=['POST'])
@jwt_required()
def add_comment():
    data = request.get_json()
    user_id = get_jwt_identity()['id']

    if not data.get('content') or not data.get('learning_path_id'):
        return jsonify({"error": "The 'content' and 'learning_path_id' fields are required"}), 400

    learning_path = LearningPath.query.get(data['learning_path_id'])
    if not learning_path:
        return jsonify({"error": "The learning path does not exist"}), 404

    new_comment = Comment(
        content=data['content'],
        user_id=user_id,
        learning_path_id=data['learning_path_id']
    )
    db.session.add(new_comment)
    db.session.commit()

    return jsonify({"message": "Comment added successfully", "comment": repr(new_comment)}), 201

@comment_routes.route('/comments/<int:learning_path_id>', methods=['GET'])
def get_comments(learning_path_id):
    comments = Comment.query.filter_by(learning_path_id=learning_path_id).all()
    if not comments:
        return jsonify({"message": "No comments for this learning path"}), 404

    comments_data = [
        {
            'id': comment.id,
            'content': comment.content,
            'date_comment': comment.date_comment.isoformat(),
            'user_id': comment.user_id
        }
        for comment in comments
    ]

    return jsonify(comments_data), 200

@comment_routes.route('/comments/<int:comment_id>', methods=['PUT'])
@jwt_required()
def update_comment(comment_id):
    data = request.get_json()
    user_id = get_jwt_identity()['id']

    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({"error": "The comment does not exist"}), 404

    if comment.user_id != user_id:
        return jsonify({"error": "You do not have permission to update this comment"}), 403

    comment.content = data.get('content', comment.content)
    db.session.commit()

    return jsonify({"message": "Comment updated successfully", "comment": repr(comment)}), 200

@comment_routes.route('/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    user_id = get_jwt_identity()['id']

    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({"error": "The comment does not exist"}), 404

    if comment.user_id != user_id:
        return jsonify({"error": "You do not have permission to delete this comment"}), 403

    db.session.delete(comment)
    db.session.commit()

    return jsonify({"message": "Comment deleted successfully"}), 200
