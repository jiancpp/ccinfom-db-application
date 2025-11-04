from flask import Flask, render_template, session, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'change-this-secret-key-123'

# ============================================
#           DATABASE CONFIGURATION
# ============================================
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',          # Change this
    'password': 'your_password',  # Change this
    'database': 'dbApp'
}

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
    return render_template('events.html')


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


# ============================================
#           ENTRY POINT
# ============================================
if __name__ == '__main__':
    app.run(debug=True)
