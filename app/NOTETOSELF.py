# In your app setup =================================
# from flask_sqlalchemy import SQLAlchemy
# from app.models import db
# db.init_app(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = ...
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = ...

# Files / folders =====================================
# models.py (if it only contained ORM models)
# migrations/ (Alembic-related)
# instance/ (if used only for SQLAlchemy-generated DB)
# Any remaining ORM-based code like User.query.filter()


# Remove from requirements.txt: ======================
    # Flask-SQLAlchemy
    # SQLAlchemy
# You only need:
    # mysql-connector-python
    # Flask
