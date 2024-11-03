from flask import Flask
from .models import db
from .controllers.user_controller import user_routes
from .controllers.auth_controller import auth_routes
from .controllers.category_controller import category_routes
from .controllers.learning_path_controller import learning_path_routes
from .controllers.level_controller import level_routes
from .controllers.comment_controller import comment_routes
from config import Config
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    jwt = JWTManager(app)

    migrate = Migrate(app, db)

    app.register_blueprint(user_routes)
    app.register_blueprint(auth_routes)
    app.register_blueprint(category_routes)
    app.register_blueprint(learning_path_routes)
    app.register_blueprint(level_routes)
    app.register_blueprint(comment_routes)

    return app