from flask import Blueprint, render_template, session, redirect, url_for, flash, g
from flask import render_template, request, redirect, url_for, jsonify

from app.models import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from sqlalchemy import func, desc

import datetime
import mysql.connector
from app.config import DB_HOST, DB_USER, DB_PASS, DB_NAME


main_routes = Blueprint('main_routes', __name__)

# ============================================
#           DATABASE CONNECTION
# ============================================
def get_conn():
    try:
        # The connect function now takes the essential credentials
        return mysql.connector.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
    except Exception as e:
        print(f"Connection failed: {e}")
        raise

def execute_query(sql, params=()):
    # Pass dictionary=True to the cursor method
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True) 
        cursor.execute(sql, params)
        
        # Results will be a list of dictionaries
        results = cursor.fetchall()
        cursor.close()
        return results
        
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None
    
def insert_query(sql, params=()):
    # Pass dictionary=True to the cursor method
    is_successful = False

    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True) 
        cursor.execute(sql, params)
        conn.commit()
        is_successful = True
        
    except Exception as e:
        print(f"Error fetching user: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

        return is_successful

# ============================================
#           CORE PAGES
# ============================================
@main_routes.route('/')
def index():
   
    events, artists = [], []
    title = ""

    follower_count = db.session.query(
        Artist_Follower.Artist_ID,
        func.count(Artist_Follower.Fan_ID).label('num_followers')
    ).group_by(Artist_Follower.Artist_ID).subquery()
    
    if g.get('current_user'):
        title = "Followed Artists"
        artists = Artist.query.join(Artist.followers).filter(
            Artist_Follower.Fan_ID == g.current_user.Fan_ID
        ).all()
    else:
        title = "Active Artists"
        artists = Artist.query.filter(
            Artist.Activity_Status == 'Active'
        ).outerjoin(
            follower_count, Artist.Artist_ID == follower_count.c.Artist_ID
        ).order_by(
            desc(follower_count.c.num_followers)
        ).limit(5).all()

    event_query = '''
    SELECT * FROM Event as e
    WHERE e.Start_Date >= CURDATE()
    ORDER BY e.Start_Date ASC
    '''
    events = execute_query(event_query)

    return render_template('index.html', artists=artists, events=events, title=title)

@main_routes.route('/artists', methods=['GET'])
def artists():
    
    current_filter = request.args.get('filter', 'all') 
    current_search = request.args.get('artist-name', '').strip()

    artists_query = Artist.query.options(
        joinedload(Artist.manager), 
        joinedload(Artist.followers) 
    )
    
    # 1. Apply search filter
    if current_search:
        artists_query = artists_query.filter(Artist.Artist_Name.ilike(f'%{current_search}%'))

    artists_list = []
    followed_artist_ids = set() # Use a set for fast lookup

    # 2. Check if a user is logged in
    if g.get('current_user'):
        current_fan_id = g.current_user.Fan_ID
        
        # Optimize: Fetch ALL followed Artist IDs for the user in ONE query
        followed_artist_ids_tuples = db.session.query(Artist_Follower.Artist_ID).filter(
            Artist_Follower.Fan_ID == current_fan_id
        ).all()
        
        followed_artist_ids = {artist_id for (artist_id,) in followed_artist_ids_tuples}
        
        # 3. Apply Follow/Not-Follow filter BEFORE executing the query
        if current_filter == 'followed':
            artists_query = artists_query.filter(Artist.Artist_ID.in_(followed_artist_ids))
        
        elif current_filter == 'not-followed':
            artists_query = artists_query.filter(Artist.Artist_ID.notin_(followed_artist_ids))
    
    # Execute the final, filtered query
    artists_list = artists_query.order_by(Artist.Artist_Name).all()
    
    # 4. Attach the 'is_followed' flag to the returned objects
    # This step is essential for the Jinja template's conditional logic.
    if g.get('current_user'):
        for artist in artists_list:
            # Dynamically attach the 'is_followed' attribute
            artist.is_followed = artist.Artist_ID in followed_artist_ids

    return render_template(
        'artists.html', 
        artists=artists_list,
        current_filter=current_filter,
        current_search=current_search
    )

@main_routes.route('/events', methods=["GET", "POST"])
def events():

    filter_condition = ""
    search_condition = ""
    query_parameters = []
    
    # Filtering events
    search_term = request.form.get("event-name", "").strip()
    filter = request.form.get("filter", "all-events")

    # ----------------------------------------------------
    # APPLY EVENT TYPE FILTER 
    # ----------------------------------------------------     
    if filter == 'artist-events':
        filter_condition = '''
        AND Event_ID IN (
            SELECT DISTINCT Event_ID 
            FROM Artist_Event
        )
        '''

    if filter == 'fanclub-events':
        filter_condition = '''
            AND Event_ID IN (
            SELECT DISTINCT Event_ID 
            FROM Fanclub_Event
        )
        '''
    # ----------------------------------------------------
    # APPLY TEXT SEARCH FILTER 
    # ----------------------------------------------------

    if search_term:
        search_condition = "AND Event_Name LIKE %s"
        search_pattern = f"%{search_term}%"
        query_parameters.append(search_pattern)
        
    
    event_query = f'''
    SELECT e.*, v.Venue_Name 
    FROM Event AS e JOIN Venue AS v ON e.Venue_ID = v.Venue_ID
    WHERE e.Start_Date >= CURDATE()
        {filter_condition}
        {search_condition}
    ORDER BY e.Start_Date ASC
    '''
    events = execute_query(event_query, tuple(query_parameters))

    return render_template(
        'events.html', 
        events=events, 
        current_filter=filter,
        current_search=search_term
    )


@main_routes.route('/merchandise')
def merchandise():
    return render_template('merchandise.html')


@main_routes.route('/fanclubs', methods=['GET'])
def fanclubs():
    current_filter = request.args.get('filter', 'all') 
    current_search = request.args.get('fanclub-name', '').strip()
    current_artist = request.args.get('artist', 'all').strip()
    
    artist_names = [artist.Artist_Name for artist in db.session.query(Artist.Artist_Name).distinct().order_by(Artist.Artist_Name).all()]
    
    base_query = db.session.query(
        Fanclub.Fanclub_ID,
        Fanclub.Fanclub_Name,
        Artist.Artist_Name.label('artist_name'),
        func.count(Fanclub_Membership.Fan_ID).label('member_count')
    ).join(Artist, Fanclub.Artist_ID == Artist.Artist_ID) \
    .outerjoin(Fanclub_Membership, Fanclub.Fanclub_ID == Fanclub_Membership.Fanclub_ID) \
    .group_by(Fanclub.Fanclub_ID, Artist.Artist_ID) \
    .order_by(Artist.Artist_Name, Fanclub.Fanclub_Name)

    if current_search:
        base_query = base_query.filter(Fanclub.Fanclub_Name.ilike(f'%{current_search}%'))

    if current_artist and current_artist != 'all':
        base_query = base_query.filter(Artist.Artist_Name == current_artist)
    
    joined_fanclub_ids = set()
    current_fan_id = None
    
    if g.get('current_user'):
        current_fan_id = g.current_user.Fan_ID

        joined_fanclub_ids_tuples = db.session.query(Fanclub_Membership.Fanclub_ID).filter(
            Fanclub_Membership.Fan_ID == current_fan_id
        ).all()

        joined_fanclub_ids = {fanclub_id for (fanclub_id,) in joined_fanclub_ids_tuples}

        if current_filter == 'joined':
            base_query = base_query.filter(Fanclub.Fanclub_ID.in_(joined_fanclub_ids))
        
        elif current_filter == 'not-joined':
            base_query = base_query.filter(Fanclub.Fanclub_ID.notin_(joined_fanclub_ids))

    fanclub_data_results = base_query.all()
    fanclubs_list = []
    
    for fanclub in fanclub_data_results:
        is_member = fanclub.Fanclub_ID in joined_fanclub_ids
        
        fanclubs_list.append({
            'fanclub_id': fanclub.Fanclub_ID,
            'fanclub_name': fanclub.Fanclub_Name,
            'artist_name': fanclub.artist_name,
            'member_count': fanclub.member_count,
            'is_member': is_member
        })

    return render_template(
        'fanclubs.html', 
        fanclubs=fanclubs_list,
        current_filter=current_filter,
        current_search=current_search,
        current_artist=current_artist, 
        artist_names=artist_names     
    )


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
                First_Name=first_name,
                Last_Name=last_name,
                Username=username,
                Email=email,
            )

            db.session.add(new_fan)
            db.session.commit()

            flash(f'Welcome, {username}! You can now log in.', 'success')
            return redirect(url_for('main_routes.login'))
        
        except Exception:
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
    event = None
    ticket_tiers = None
    tier_sections = {}

    # Fetch record from database
    event_query = '''
    SELECT * 
    FROM Event AS e JOIN Venue AS v ON e.Venue_ID = v.Venue_ID
    WHERE e.Event_ID = %s
    '''

    # Error handling
    event_results = execute_query(event_query, (event_id,))
    if event_results:
        event = event_results[0]
    if not event:
        return redirect(url_for('main_routes.events'))

    tier_query = '''
    SELECT * 
    FROM Ticket_Tier
    WHERE Event_ID = %s
    '''
    ticket_tiers = execute_query(tier_query, (event_id,))  
    if not ticket_tiers:
        # Event not found, return or redirect otherwise
        return redirect(url_for('main_routes.events'))

    for tier in ticket_tiers:
        section_query = '''
        SELECT * 
        FROM Section
        WHERE Section_ID IN (
            SELECT Section_ID 
            FROM Tier_Section
            WHERE Tier_ID = %s
        )
        '''
        sections = execute_query(section_query, (tier['Tier_ID'],))

        if sections:
            tier_sections[tier['Tier_ID']] = sections
        else:
            tier_sections[tier['Tier_ID']] = []

    # Get purchase details
    if request.method == "POST":
        tier_id = request.form["ticket_tier"]
        seat_id = request.form.get("seat_id", None)     

        if seat_id == "":
            seat_id = None   

        Fan_ID = session.get('fan_id')                 
        Event_ID = event_id
        Tier_ID = tier_id
        Seat_ID = seat_id            

        insert_ticket_purchase = '''
        INSERT INTO Ticket_Purchase (Fan_ID, Event_ID, Tier_ID, Seat_ID)
        VALUES (%s, %s, %s, %s)
        '''

        if insert_query(insert_ticket_purchase, (Fan_ID, Event_ID, Tier_ID, Seat_ID)):
            flash(f"Success! View your purchased ticket on your profile.", "success")
        else:
            flash(f"Error purchasing.", "error")

    return render_template(
        "event_details.html", 
        event=event, 
        ticket_tiers=ticket_tiers, 
        tier_sections=tier_sections)

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

@main_routes.route('/fanclub/<int:fanclub_id>/create-event', methods=['GET', 'POST'])
def create_fanclub_event(fanclub_id):
    fanclub = Fanclub.query.get_or_404(fanclub_id)
    artist = Artist.query.get(fanclub.Artist_ID) if fanclub.Artist_ID else None
    all_venues = Venue.query.order_by(Venue.Venue_Name).all()
    
    if request.method == 'GET':        
        return render_template(
            'create_fanclub_event.html', 
            fanclub=fanclub, 
            artist=artist, 
            venues=all_venues
        )

    if request.method == 'POST':
        try:
            event_name = request.form.get('event_name')
            event_type = request.form.get('event_type')
            venue_id = request.form.get('venue_id')
            start_date_str = request.form.get('start_date')
            end_date_str = request.form.get('end_date')
            start_time_str = request.form.get('start_time')
            end_time_str = request.form.get('end_time')
            
            if not all([event_name, event_type, venue_id, start_date_str, start_time_str, end_time_str]):
                flash("Missing required event information.", 'error')
                return redirect(request.url)
            
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            start_time = datetime.datetime.strptime(start_time_str, '%H:%M').time()
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else start_date
            end_time = datetime.datetime.strptime(end_time_str, '%H:%M').time()

            new_event = Event(
                Event_Name=event_name,
                Event_Type=event_type,
                Venue_ID=venue_id,
                Start_Date=start_date,
                End_Date=end_date,
                Start_Time=start_time,
                End_Time=end_time
            )


            db.session.add(new_event)
            db.session.flush()

            default_tier = Ticket_Tier(
                Event_ID=new_event.Event_ID
            )
            db.session.add(default_tier)
            db.session.flush()

            new_fanclub_event = Fanclub_Event(
                Fanclub_ID=fanclub.Fanclub_ID,
                Event_ID=new_event.Event_ID
            )

            db.session.add(new_fanclub_event)
            db.session.commit()
            
            flash(f"Event '{event_name}' successfully created!", 'success')
            return redirect(url_for('main_routes.fanclub_details', fanclub_id=fanclub_id))

        except IntegrityError as e:
            db.session.rollback()
            flash(f"Database Error (Integrity constraint failed). Please check inputs.", 'error')
            print(f"SQLAlchemy Integrity Error: {e}")
        except Exception as e:
            db.session.rollback()
            flash(f"An unexpected error occurred. {e}", 'error')

        artist = Artist.query.get(fanclub.Artist_ID) if fanclub.Artist_ID else None
        all_venues = Venue.query.order_by(Venue.Venue_Name).all()

        return render_template('create_fanclub_event.html', 
            fanclub=fanclub, 
            artist=artist, 
            venues=all_venues
        )
    
# ============================================
#           Artist Subpages
# ============================================
@main_routes.route('/artists/<int:artist_id>')
def artist_details(artist_id):
    artist = Artist.query.options(
        joinedload(Artist.manager),          
        joinedload(Artist.member_detail),      
        joinedload(Artist.events).joinedload(Event.venue),
        joinedload(Artist.fanclubs).joinedload(Fanclub.fanclub_memberships),
        joinedload(Artist.merchandise)
    ).get_or_404(artist_id)
    
    artist.is_followed = False
    
    if g.get('current_user'):
        is_following_query = db.session.query(Artist_Follower).filter(
            Artist_Follower.Fan_ID == g.current_user.Fan_ID,
            Artist_Follower.Artist_ID == artist_id
        ).one_or_none()
        
        # Assign the boolean result to the new attribute
        artist.is_followed = is_following_query is not None
        
    return render_template(
        'artist_details.html', 
        artist=artist,
    )

@main_routes.route('/artists/toggle_follow/<int:artist_id>', methods=['POST'])
def toggle_follow(artist_id):
    if not g.get('current_user'):
        flash("You must be logged in to follow an artist.", 'error')
        # Redirect to login, but store 'next' URL (not shown, but good practice)
        return redirect(url_for('main_routes.login'))

    artist = Artist.query.get_or_404(artist_id)
    current_fan_id = g.current_user.Fan_ID
    
    # Get the action from the hidden input field in the POST request
    action = request.form.get('action') 

    # Check for existing follow relationship
    follow_entry = db.session.query(Artist_Follower).filter(
        Artist_Follower.Fan_ID == current_fan_id,
        Artist_Follower.Artist_ID == artist_id
    ).one_or_none()
    
    if action == 'follow' and not follow_entry:
        # User requested to follow and isn't following yet
        new_follow = Artist_Follower(Fan_ID=current_fan_id, Artist_ID=artist_id)
        db.session.add(new_follow)
        db.session.commit()
        flash(f"🎉 You are now following {artist.Artist_Name}! ", 'success')
        
    elif action == 'unfollow' and follow_entry:
        # User requested to unfollow and is currently following
        db.session.delete(follow_entry)
        db.session.commit()
        flash(f"💔 You have unfollowed {artist.Artist_Name}.", 'info')
        
    # Redirect back to the page the user came from (artists list or details page)
    return redirect(request.referrer or url_for('main_routes.artists'))