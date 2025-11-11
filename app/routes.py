from flask import Blueprint, render_template, session, redirect, url_for, flash, g
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


@main_routes.route('/events', methods=["GET", "POST"])
def events():
    event_query = Event.query

    # Filtering events
    search_term = request.form.get("event-name", "").strip()
    filter = request.form.get("filter", "all-events")

    # ----------------------------------------------------
    # APPLY EVENT TYPE FILTER 
    # ----------------------------------------------------     
    if filter == 'artist-events':
        event_query = Event.query.filter(Event.artists.any())

    if filter == 'fanclub-events':
            event_query = Event.query.filter(Event.fanclubs.any())

    # ----------------------------------------------------
    # APPLY TEXT SEARCH FILTER 
    # ----------------------------------------------------

    if search_term:
        search_pattern = f"%{search_term}%"
        event_query = event_query.filter(
            Event.Event_Name.ilike(search_pattern)    # for case insensitive search
        )        

    events = event_query.all()

    return render_template('events.html', events=events, current_filter=filter)


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
        is_member = Fanclub_Membership.query.filter_by(Fanclub_ID=fanclub_id, Fan_ID=g.current_user.Fan_ID).first() is not None
        
        fanclubs_list.append({
            'fanclub_id': fanclub_id,
            'fanclub_name': fanclub_name,
            'artist_name': artist_name,
            'member_count': member_count,
            'is_member': is_member
        })

    return render_template('fanclubs.html', fanclubs=fanclubs_list)


# ============================================
#           USER MANAGEMENT (PLACEHOLDERS)
# ============================================
@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form.get('username')
        
        fan = Fan.query.filter(
            (Fan.Username == username_or_email) | (Fan.Email == username_or_email)
        ).first()

        if fan:
            session['logged_in'] = True
            session['username'] = fan.Username
            session['fan_id'] = fan.Fan_ID
            
            flash(f'Login successful! Welcome back, {fan.First_Name}.', 'success')
            return redirect(url_for('main_routes.index')) 
        else:
            flash('Login failed: Account with that username or email not found.', 'error')
            
    return render_template('login.html')

@main_routes.route('/logout')
def logout():
    session.pop('fan_id', None)
    session.pop('username', None)
    session.pop('logged_in', None)
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('main_routes.index'))


@main_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('username')
        email = request.form.get('email')
        
        if not all([first_name, last_name, username, email]):
            flash('All fields are required. Did you forget something?', 'error')
            return redirect(url_for('main_routes.register'))

        if Fan.query.filter_by(Username=username).first():
            flash('An account with that username already exists. Try logging in!', 'error')
            return redirect(url_for('main_routes.register'))

        if Fan.query.filter_by(Email=email).first():
            flash('An account with that email already exists. Try logging in!', 'error')
            return redirect(url_for('main_routes.register'))

        try:
            new_fan = Fan(
                first_name=first_name, 
                last_name=last_name, 
                username=username, 
                email=email,
            )
            db.session.add(new_fan)
            db.session.commit()

            flash(f'Welcome, {username}! You can now log in.', 'success')
            return redirect(url_for('main_routes.login'))
        
        except Exception as e:
            db.session.rollback()
            flash('A server error occurred during registration. Please try again.', 'error')

    return render_template('register.html')


@main_routes.route('/profile')
def profile():
    current_fan_id = session.get('fan_id')
    fan = Fan.query.get(current_fan_id)

    memberships = fan.memberships
    purchases = fan.ticket_purchases

    return render_template('profile.html', fan=fan, memberships=memberships, purchases=purchases)


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
            Fan_ID = session.get('fan_id'),                 # Change to session.fan_id or something later
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
    
    merch_list = Merchandise.query.filter_by(Fanclub_ID=fanclub_id).all()
    
    is_member = Fanclub_Membership.query.filter_by(Fanclub_ID=fanclub_id, Fan_ID=g.current_user.Fan_ID).first() is not None

    context = {
        'fanclub_id': club.Fanclub_ID,
        'fanclub_name': club.Fanclub_Name,
        'artist_id': club.Artist_ID,
        'artist_name': artist_name,
        'member_count': member_count,
        'is_member': is_member,
        'merchandise': [{'merch_name': m.Merchandise_Name, 'price': m.Merchandise_Price, 'merch_ID': m.Merchandise_ID} for m in merch_list],
        'events': [{'event_name': e.Event_Name, 'start_date': e.Start_Date, 'end_date': e.End_Date, 'event_id': e.Event_ID} for e in event_list],
    }
    
    return render_template('fanclub_details.html', fanclub=context)


@main_routes.route('/fanclubs/<int:fanclub_id>/members')
# @login_required # Ensure only logged-in users can view the list
def fanclub_members(fanclub_id):
    club = Fanclub.query.filter_by(Fanclub_ID=fanclub_id).first_or_404()
    
    is_member = Fanclub_Membership.query.filter_by(Fanclub_ID=fanclub_id, Fan_ID=g.current_user.Fan_ID).first() is not None
    
    if not is_member:
        flash(f"You must be a member of {club.Fanclub_Name} to view this.", 'error')
        return redirect(url_for('main_routes.fanclub_details', fanclub_id=fanclub_id))


    members_data = db.session.query(
        Fan.Username, 
        Fan.Date_Joined
    ) \
        .join(Fanclub_Membership, Fan.Fan_ID == Fanclub_Membership.Fan_ID) \
        .filter(Fanclub_Membership.Fanclub_ID == club.Fanclub_ID) \
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
    membership = Fanclub_Membership(Fanclub_ID=fanclub_id, Fan_ID=g.current_user.Fan_ID)
    db.session.add(membership)
    db.session.commit()
    
    flash(f"You successfully joined this fanclub!", "success")
    return redirect(url_for('main_routes.fanclub_details', fanclub_id=fanclub_id))

@main_routes.route('/fanclubs/<int:fanclub_id>/leave', methods=['POST'])
def leave_fanclub(fanclub_id):
    membership = Fanclub_Membership.query.filter_by(Fanclub_ID=fanclub_id, Fan_ID=g.current_user.Fan_ID).first()
    db.session.delete(membership)
    db.session.commit()
        
    flash(f"You successfully left this fanclub.", "success")
    return redirect(url_for('main_routes.fanclub_details', fanclub_id=fanclub_id))