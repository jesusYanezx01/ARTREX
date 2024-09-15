from flask import Flask
from .models import db
from .routes import routes
from config import Config
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    migrate = Migrate(app, db)

    app.register_blueprint(routes)

    return app