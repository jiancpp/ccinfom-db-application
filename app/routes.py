from flask import Blueprint, render_template, session, redirect, url_for, flash
from flask import render_template, request, redirect, url_for, jsonify

from app.models import *


main_routes = Blueprint('main_routes', __name__)

# ============================================
#           CORE PAGES
# ============================================
@main_routes.route('/')
def index():
    #added
    artists, events = [], []
    tier = Ticket_Tier.query.get(10)  
    if tier:
        print([s.Section_Name for s in tier.sections])
    else:
        print("error")

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

@main_routes.route('/events/buy_ticket/<int:event_id>', methods=["GET", "POST"])
def buy_ticket(event_id):
    event = Event.query.get_or_404(event_id)

    if request.method == "POST":
        tier_id = request.form["ticket_tier"]
        seat_id = request.form.get("seat_id", None)     

        if seat_id == "":
            seat_id = None   

        purchase = Ticket_Purchase(
            Fan_ID = 1,                 # Change to session.fan_id or something later
            Event_ID = event.Event_ID,
            Tier_ID = tier_id,
            Seat_ID = seat_id            
        )


        db.session.add(purchase)
        db.session.commit()

        

    return render_template("events_ticket_purchase.html", event=event)

@main_routes.route('/events/buy_ticket/<int:event_id>/<int:section_id>/seats', methods=["GET"])
def get_seats(event_id, section_id):
    """
    Paginated seats for a given section
    ?page=1&per_page=450
    """
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 450, type=int)

    query = (
        db.session.query(Seat.Seat_ID, Seat.Seat_Row, Seat.Seat_Number)
        .filter(Seat.Section_ID == section_id)\
        .order_by(Seat.Seat_ID)
    )

    total = query.count()

    # skips a number of records before returning results
    seats = query.offset((page - 1) * per_page).limit(per_page).all()

    seat_list = [
        { "id": s.Seat_ID, "seat_row": s.Seat_Row, "seat_number": s.Seat_Number }
        for s in seats
    ]

    return jsonify({
        "page": page,
        "per_page": per_page,
        "total": total,
        "seats": seat_list
    })
