from flask import g, session
from .models import db, Fan

def load_logged_in_user():
    fan_id = session.get('fan_id')

    if fan_id is None:
        g.current_user = None
    else:
        g.current_user = db.session.get(Fan, fan_id)

def inject_user():
    return dict(current_user=g.current_user)