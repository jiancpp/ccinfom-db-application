from flask import Flask, g, session
from app.config import DB_USER, DB_PASS, DB_NAME

from .db_utils import execute_select_query

def load_logged_in_user():
    fan_id = session.get('fan_id')

    query = '''
        SELECT Fan_ID, First_Name, Username, Email
        FROM Fan
        WHERE Fan_ID = %s
    '''
    result = execute_select_query(query, (fan_id,))

    if result:
        g.current_user = result[0]
    else:
        g.current_user = None

def inject_user():
    return dict(current_user=g.current_user)

def create_app():
    app = Flask(__name__)

    app.config['DB_USER'] = DB_USER
    app.config['DB_PASS'] = DB_PASS
    app.config['DB_NAME'] = DB_NAME
    app.secret_key = 'secret-key'

    app.before_request(load_logged_in_user)
    app.context_processor(inject_user)

    from .routes import main_routes
    app.register_blueprint(main_routes)

    return app