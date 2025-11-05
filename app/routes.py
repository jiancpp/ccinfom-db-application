from flask import Blueprint, render_template, session, redirect, url_for, flash
from app.models import *


main_routes = Blueprint('main_routes', __name__)

# ============================================
#           CORE PAGES
# ============================================
@main_routes.route('/')
def index():
    artists, events = [], []
    return render_template('index.html', artists=artists, events=events)


@main_routes.route('/artists')
def artists():    
    return render_template('artists.html')


@main_routes.route('/events')
def events():
    events = Event.query.all()
    return render_template('events.html', events=events)


@main_routes.route('/merchandise')
def merchandise():
    return render_template('merchandise.html')


@main_routes.route('/fanclubs')
def fanclubs():
    return render_template('fanclubs.html')



# ============================================
#           USER MANAGEMENT (PLACEHOLDERS)
# ============================================
@main_routes.route('/login')
def login():
    # Setup login later
    session["username"] = "Person"
    return render_template('login.html')


@main_routes.route('/register')
def register():
    return render_template('register.html')


@main_routes.route('/profile')
def profile():
    return render_template('profile.html')


@main_routes.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@main_routes.route('/test_db')
def test_db():
    import mysql.connector
    from app.config import DB_CONFIG

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT DATABASE();")
    current_db = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM Event;")
    event_count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return f"Connected to: {current_db}, found {event_count} events."


# ============================================
#           Event Subpages
# ============================================

@main_routes.route('/buy_ticket/<int:event_id>')
def buy_ticket(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template("events_ticket_purchase.html", event=event)
