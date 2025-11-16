from flask import Flask, g, session
from app.config import DB_USER, DB_PASS, DB_NAME
from app.user_loader import load_logged_in_user, inject_user

# =========== REMOVE LATER ===================
from flask_sqlalchemy import SQLAlchemy 
from app.models import db

def create_app():
    # ==================== DELETE LATER ======================= 
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{DB_USER}:{DB_PASS}@localhost/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = "your_secret_key"
    db.init_app(app)
    # ========================================================

    # ================= REPLACE WITH [OPTIONAL] =================
    # app.config['DB_USER'] = DB_USER
    # app.config['DB_PASS'] = DB_PASS
    # app.config['DB_NAME'] = DB_NAME


    app.before_request(load_logged_in_user)
    app.context_processor(inject_user)

    from .routes import main_routes
    app.register_blueprint(main_routes)

    return app