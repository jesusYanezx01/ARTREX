from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.models import User, LearningPath
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

recommendation_routes = Blueprint('recommendation_routes', __name__)

@recommendation_routes.route('/recommendation/<int:user_id>', methods=['GET'])
@jwt_required()
def recommend(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found."}), 404

    user_tags = get_user_tags(user)
    if not user_tags:
        return jsonify({"message": "User has no learning history."}), 400

    learning_paths = load_learning_paths()

    if learning_paths.empty:
        return jsonify({"message": "No learning paths available."}), 400

    # TF-IDF Vectorization
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(learning_paths['tags'])

    # User vector
    user_vec = tfidf.transform([user_tags])

    # Calculate similarity
    similarities = cosine_similarity(user_vec, tfidf_matrix)

    # Select top 5
    top_n = 5
    similar_indices = similarities[0].argsort()[-top_n:][::-1]

    recommended_paths = learning_paths.iloc[similar_indices]

    return jsonify(recommended_paths.to_dict(orient='records')), 200

def load_learning_paths():
    """
    Loads all LearningPaths along with their Labels into a DataFrame.    
    """
    learning_paths = LearningPath.query.all()

    paths_data = []
    for path in learning_paths:
        tags = " ".join([label.name for label in path.labels])
        paths_data.append({
            'id': path.id,
            'name': path.title,
            'tags': tags
        })

    return pd.DataFrame(paths_data)

def get_user_tags(user):
    """
    Builds user tags based on the LearningPaths where they have had Scores.   
    """
    if not user.scores:
        return None

    user_labels = []
    for score in user.scores:
        path = LearningPath.query.get(score.learning_path_id)
        if path and path.labels:
            user_labels.extend([label.name for label in path.labels])

    if not user_labels:
        return None

    return " ".join(user_labels)