from flask import Flask, render_template, session, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

from model.config import DB_CONFIG

app = Flask(__name__)
app.secret_key = 'change-this-secret-key-123'

def get_db_connection():
    """Return a MySQL connection or None on failure."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Database Error: {e}")
        return None


# ============================================
#           CORE PAGES
# ============================================
@app.route('/')
def index():
    conn = get_db_connection()
    artists, events = [], []

    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.close()
        conn.close()

    return render_template('index.html', artists=artists, events=events)


@app.route('/artists')
def artists():    
    return render_template('artists.html')


@app.route('/events')
def events():
    conn = get_db_connection()
    events = []

    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT Event_Name, Start_Date
            FROM Event
            ORDER BY Event_Name
            """
        )
        events = cursor.fetchall()
        cursor.close()
        conn.close()

    return render_template('events.html', events=events)


@app.route('/merchandise')
def shop():
    return render_template('merchandise.html')


@app.route('/fanclubs')
def fanclubs():
    return render_template('fanclubs.html')



# ============================================
#           USER MANAGEMENT (PLACEHOLDERS)
# ============================================
@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/test_db')
def test_db():
    import mysql.connector
    from model.config import DB_CONFIG

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
#           ENTRY POINT
# ============================================
if __name__ == '__main__':
    app.run(debug=True)
    
