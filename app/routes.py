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
    artists = Artist.query.all()
    return render_template('artists.html', artists=artists)


@main_routes.route('/events')
def events():
    events = Event.query.all()
    return render_template('events.html', events=events)


@main_routes.route('/merchandise')
def merchandise():
    return render_template('merchandise.html')


@main_routes.route('/fanclubs')
def fanclubs():
    fanclub_data = db.session.query(
            Fanclub.Fanclub_ID,
            Fanclub.Fanclub_Name,
            Artist.Artist_Name.label('artist_name'),
            func.count(Fanclub_Membership.Fan_ID).label('member_count')
        ).join(Artist, Fanclub.Artist_ID == Artist.Artist_ID) \
        .outerjoin(Fanclub_Membership, Fanclub.Fanclub_ID == Fanclub_Membership.Fanclub_ID) \
        .group_by(Fanclub.Fanclub_ID, Artist.Artist_ID) \
        .order_by(Artist.Artist_Name, Fanclub.Fanclub_Name) \
        .all()
    
    fanclubs_list = []
    for fanclub_id, fanclub_name, artist_name, member_count in fanclub_data:
        is_member = False 
        # if current_user.is_authenticated:
        #    is_member = Fanclub_Membership.query.filter_by(Fanclub_ID=fanclub_id, Fan_ID=current_user.Fan_ID).first() is not None
        
        fanclubs_list.append({
            'Fanclub_ID': fanclub_id,
            'Fanclub_Name': fanclub_name,
            'artist_name': artist_name,
            'member_count': member_count,
            'is_member': is_member
        })

    return render_template('fanclubs.html', fanclubs=fanclubs_list)


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

# ============================================
#           Fanclub Subpages
# ============================================

@main_routes.route('/fanclubs/<int:fanclub_id>')
def fanclub_details(fanclub_id):
    fanclub_query = Fanclub.query.join(Artist, Fanclub.Artist_ID == Artist.Artist_ID) \
        .filter(Fanclub.Fanclub_ID == fanclub_id) \
        .with_entities(Fanclub, Artist.Artist_Name.label('artist_name')).first_or_404()
    
    club, artist_name = fanclub_query

    member_count = Fanclub_Membership.query.filter_by(Fanclub_ID=fanclub_id).count()
    event_list = club.events
    
    merch_list = Merchandise.query.filter_by(Artist_ID=club.Artist_ID).all()
    
    is_member = False 

    context = {
        'Fanclub_ID': club.Fanclub_ID,
        'Fanclub_Name': club.Fanclub_Name,
        'Artist_ID': club.Artist_ID,
        'artist_name': artist_name,
        'member_count': member_count,
        'is_member': is_member,
        'merchandise': [{'Merch_Name': m.Merchandise_Name, 'Price': m.Merchandise_Price, 'Merch_ID': m.Merchandise_ID} for m in merch_list],
        'events': [{'Event_Name': e.Event_Name, 'Event_Date': e.Start_Date, 'Event_ID': e.Event_ID} for e in event_list],
    }
    
    return render_template('fanclub_details.html', fanclub=context)


@main_routes.route('/fanclubs/<int:fanclub_id>/members')
# @login_required # Ensure only logged-in users can view the list
def fanclub_members(fanclub_id):
    club = Fanclub.query.filter_by(Fanclub_ID=fanclub_id).first_or_404()
    
    # is_member = Fanclub_Membership.query.filter_by(
    #     Fanclub_ID=fanclub_id,
    #     User_ID=current_user.User_ID 
    # ).first()
    
    # if not is_member:
    #     flash(f"You must be a member of {club.Fanclub_Name} to view the community list.", 'danger')
    #     return redirect(url_for('main_routes.fanclub_details', fanclub_id=fanclub_id))


    members_data = db.session.query(
        Fan.Username, 
        Fan.Date_Joined
    ) \
        .join(Fanclub_Membership, Fan.Fan_ID == Fanclub_Membership.Fan_ID) \
        .filter(Fanclub_Membership.Fanclub_ID == fanclub_id) \
        .all()
    
    context = {
        'fanclub_id': club.Fanclub_ID,
        'fanclub_name': club.Fanclub_Name,
        'members': [
            {'username': name, 'join_date': date.strftime('%Y-%m-%d')} 
            for name, date in members_data
        ]
    }
    
    return render_template('fanclub_members.html', fanclub=context)


@main_routes.route('/fanclubs/<int:fanclub_id>/join', methods=['POST'])
def join_fanclub(fanclub_id):
    # if not current_user.is_authenticated:
    #     flash("Please log in to join a fanclub.", "danger")
    #     return redirect(url_for('auth_routes.login'))

    # membership = Fanclub_Membership(Fanclub_ID=fanclub_id, Fan_ID=current_user.Fan_ID)
    # db.session.add(membership)
    # db.session.commit()
    
    flash(f"You successfully joined Fanclub ID {fanclub_id}! (Action Placeholder)", "success")
    return redirect(url_for('main_routes.fanclub_details', fanclub_id=fanclub_id))

@main_routes.route('/fanclubs/<int:fanclub_id>/leave', methods=['POST'])
def leave_fanclub(fanclub_id):
    # membership = Fanclub_Membership.query.filter_by(Fanclub_ID=fanclub_id, Fan_ID=current_user.Fan_ID).first()
    # if membership:
    #     db.session.delete(membership)
    #     db.session.commit()
        
    flash(f"You successfully left Fanclub ID {fanclub_id}. (Action Placeholder)", "warning")
    return redirect(url_for('main_routes.fanclub_details', fanclub_id=fanclub_id))