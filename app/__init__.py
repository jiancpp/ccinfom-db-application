from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.config import DB_USER, DB_PASS, DB_NAME
from app.models import db


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{DB_USER}:{DB_PASS}@localhost/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = "your_secret_key"

    db.init_app(app)

    # Import and register routes
    from .routes import main_routes
    app.register_blueprint(main_routes)

    return app