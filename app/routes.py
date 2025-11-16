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

def execute_select_query(sql, params=()):
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
        return []
    
def execute_insert_query(sql, params=()):
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
   
    title = ""
    artist_query = ""
    event_label = ""
    
    if g.get('current_user'):
            title = "Artists You Follow"
            fan_ID = g.current_user.Fan_ID
            artist_query = '''
                SELECT * FROM Artist AS a
                JOIN Artist_Follower AS af ON a.Artist_ID = af.Artist_ID
                WHERE af.Fan_ID = %s
                ORDER BY a.Artist_Name ASC;
                '''
            total_artists_query = '''
                SELECT COUNT(*) AS Total_Artists FROM Artist_Follower
                WHERE Fan_ID = %s;
                '''
            artists = execute_select_query(artist_query, (fan_ID,))
            total_artists = execute_select_query(total_artists_query, (fan_ID,))
            
            if total_artists:
                total_artists = total_artists[0]['Total_Artists']
            else :
                total_artists = 0

            event_label = "Attending Events"
            event_query = '''
            SELECT DISTINCT e.* FROM Event AS e
            LEFT JOIN Ticket_Purchase tp ON e.Event_ID = tp.Event_ID
            WHERE e.Start_Date >= CURDATE() AND tp.Fan_ID = %s
            ORDER BY e.Start_Date ASC
            LIMIT 5;
            '''
            events = execute_select_query(event_query, (fan_ID,))

    else:
        title = "Popular Artists"
        artist_query = '''
            SELECT a.*, COUNT(af.Fan_ID) AS Num_Followers FROM Artist AS a
            LEFT JOIN Artist_Follower AS af ON a.Artist_ID = af.Artist_ID
            WHERE a.Activity_Status = 'Active'
            GROUP BY a.Artist_ID, a.Artist_Name
            ORDER BY num_followers DESC
            LIMIT 5;
            '''
        artists = execute_select_query(artist_query)
        total_artists = 5

        event_label = "Upcoming Events"
        event_query = '''
            SELECT * FROM Event AS e
            WHERE e.Start_Date >= CURDATE() 
            AND e.Start_Date < DATE_ADD(LAST_DAY(CURDATE()), INTERVAL 1 MONTH)
            ORDER BY e.Start_Date ASC
            '''
        events = execute_select_query(event_query)

    return render_template(
        'index.html', 
        artists=artists, 
        events=events, 
        total_artists=total_artists, 
        title=title,
        event_label=event_label)

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

    return render_template(
        'artists.html', 
        artists=artists_list,
        current_filter=current_filter,
        current_search=current_search
    )

@main_routes.route('/events', methods=["GET", "POST"])
def events():

    join_condition = ""
    filter_condition = ""
    search_condition = ""
    query_parameters = []
    event_types = {}
    
    # Filtering events
    search_term = request.form.get("event-name", "").strip()
    filter = request.form.get("filter", "all-events")

    # ----------------------------------------------------
    # APPLY EVENT TYPE FILTER 
    # ----------------------------------------------------     
    if filter == 'artist-events':
        filter_condition = "AND a.Artist_Name IS NOT NULL"

    if filter == 'fanclub-events':
        filter_condition = "AND f.Fanclub_Name IS NOT NULL"
    # ----------------------------------------------------
    # APPLY TEXT SEARCH FILTER 
    # ----------------------------------------------------

    if search_term:
        search_condition = '''
        AND (
            e.Event_Name LIKE %s 
            OR COALESCE(fa.Artist_Name,'') LIKE %s 
            OR COALESCE(a.Artist_Name,'') LIKE %s 
            OR COALESCE(f.Fanclub_Name,'') LIKE %s
        )
        '''
        search_pattern = f"%{search_term}%"
        query_parameters.append(search_pattern)
        query_parameters.append(search_pattern)
        query_parameters.append(search_pattern)
        query_parameters.append(search_pattern)
        
    event_query = f'''
    SELECT DISTINCT e.*, 
           v.Venue_Name
    FROM Event AS e 
        JOIN Venue AS v ON e.Venue_ID = v.Venue_ID
        LEFT JOIN Artist_Event ae ON e.Event_ID = ae.Event_ID
        LEFT JOIN Artist a ON ae.Artist_ID = a.Artist_ID
        LEFT JOIN Fanclub_Event fe ON e.Event_ID = fe.Event_ID
        LEFT JOIN Fanclub f ON fe.Fanclub_ID = f.Fanclub_ID
        LEFT JOIN Artist fa ON f.Artist_ID = fa.Artist_ID
    WHERE e.Start_Date >= CURDATE()
        {filter_condition}
        {search_condition}
    ORDER BY e.Start_Date ASC
    '''
    events = execute_select_query(event_query, tuple(query_parameters))

    for event in events:
        type_query = '''
        SELECT l.Event_ID, r.*
        FROM LINK_Event_Type l
        JOIN REF_Event_Type r ON r.Type_ID = l.Type_ID
        WHERE l.Event_ID = %s
        '''

        types = execute_select_query(type_query, (event['Event_ID'],))
        if types:
            event_types[event['Event_ID']] = types
        else:
            event_types[event['Event_ID']] = []

    return render_template(
        'events.html', 
        events=events, 
        event_types=event_types,
        current_filter=filter,
        current_search=search_term
    )


# =========================================================================
# MERCH MAIN
# =========================================================================
@main_routes.route('/merchandise')
def merchandise():
    artist_filter_id = request.args.get('artist_id', type=int)
    fanclub_filter_id = request.args.get('fanclub_id', type=int)

    merch_query = Merchandise.query.order_by(Merchandise.Merchandise_Name)
    
    # Artist Filter
    if artist_filter_id:
        merch_query = merch_query.filter(Merchandise.Artist_ID == artist_filter_id)

    # Fanclub Filter 
    if fanclub_filter_id:
        merch_query = merch_query.filter(Merchandise.Fanclub_ID == fanclub_filter_id)

    # Execute Query and Group by Artist    
    if artist_filter_id:
        artists = Artist.query.filter(Artist.Artist_ID == artist_filter_id).order_by(Artist.Artist_Name).all()
    else:
        artists = Artist.query.order_by(Artist.Artist_Name).all()
    
    
    artists_merch_data = []
    
    filtered_merchandise = merch_query.all()
    
    
    for artist in artists:
        merch_for_artist = [item for item in filtered_merchandise if item.artist == artist]
        if merch_for_artist or not (artist_filter_id or fanclub_filter_id):
            
            merch_list_data = []
            for merch_item in merch_for_artist:
                merch_list_data.append({
                    'id': merch_item.Merchandise_ID,
                    'name': merch_item.Merchandise_Name,
                    'type': merch_item.Merchandise_Description, 
                    'price': float(merch_item.Merchandise_Price),
                    'sku': f"SKU-{merch_item.Merchandise_ID}",
                    'stock': merch_item.Quantity_Stock
                })
                
            if merch_list_data:
                artists_merch_data.append({
                    'name': artist.Artist_Name,
                    'merchandise': merch_list_data
                })
                
    if fanclub_filter_id:
        fanclubs = Fanclub.query.filter(Fanclub.Fanclub_ID == fanclub_filter_id).order_by(Fanclub.Fanclub_Name).all()
    else:
        fanclubs = Fanclub.query.order_by(Fanclub.Fanclub_Name).all()
        
    for fanclub in fanclubs:
        merch_for_fanclub = [item for item in filtered_merchandise if item.fanclub == fanclub]

        if merch_for_fanclub or not (artist_filter_id or fanclub_filter_id):            
            merch_list_data = []
            for merch_item in merch_for_fanclub:
                merch_list_data.append({
                    'id': merch_item.Merchandise_ID,
                    'name': merch_item.Merchandise_Name,
                    'type': merch_item.Merchandise_Description, 
                    'price': float(merch_item.Merchandise_Price),
                    'sku': f"SKU-{merch_item.Merchandise_ID}",
                    'stock': merch_item.Quantity_Stock
                })
                
            if merch_list_data:
                artists_merch_data.append({
                    'name': fanclub.Fanclub_Name,
                    'merchandise': merch_list_data
                })
    
    all_artists_data = [{'id': a.Artist_ID, 'name': a.Artist_Name} for a in Artist.query.order_by(Artist.Artist_Name).all()]
    all_fanclubs_data = [{'id': f.Fanclub_ID, 'name': f.Fanclub_Name} for f in Fanclub.query.order_by(Fanclub.Fanclub_Name).all()]

    return render_template(
        'merchandise.html', 
        artists_merch=artists_merch_data,
        all_artists=all_artists_data,
        all_fanclubs=all_fanclubs_data,
        cart_item_count=0 
    )


@main_routes.route('/fanclubs', methods=['GET'])
def fanclubs():
    # ----------------------------------------------------
    # SETUP & INPUTS
    # ---------------------------------------------------- 
    conditions = []
    query_parameters = []

    current_fan_id = g.current_user.Fan_ID
    current_search = request.args.get('fanclub-name', '').strip()
    current_filter = request.args.get('filter', 'all') 
    current_artist = request.args.get('artist', 'all').strip()

    # ----------------------------------------------------
    # APPLY SEARCH FILTER 
    # ----------------------------------------------------     
    if current_search:
        search_condition = "f.Fanclub_Name LIKE %s"
        search_pattern = f"%{current_search}%"
        query_parameters.append(search_pattern)

    # ----------------------------------------------------
    # APPLY JOINED FANCLUBS FILTER 
    # ----------------------------------------------------     
    if current_filter == 'joined':
        conditions.append("fm.Fan_ID IS NOT NULL")

    if current_filter == 'not-joined':
        conditions.append("fm.Fan_ID IS NULL")

    # ----------------------------------------------------
    # APPLY ARTIST FANCLUBS FILTER 
    # ----------------------------------------------------     
    if current_artist != "all":
        artist_condition = "AND a.Artist_Name LIKE %s"
        artist_pattern = f"%{current_artist}%"
        query_parameters.append(artist_pattern)


    # ----------------------------------------------------
    # BUILD QUERY 
    # ----------------------------------------------------

    where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""

    artist_query = f'''
    SELECT Artist_Name 
    FROM Artist
    ORDER BY Artist_Name
    '''

    artists = execute_select_query(artist_query)

    fanclub_query = f'''
    SELECT fm.Fan_Id AS is_member_fan_id, f.Fanclub_ID, f.Fanclub_Name, a.Artist_Name, 
           COUNT(fm.Fan_Id) AS Member_Count
    FROM Fanclub AS f
        LEFT JOIN Artist AS a ON f.Artist_ID = a.Artist_ID
        LEFT JOIN Fanclub_Membership AS m ON f.Fanclub_ID = m.Fanclub_ID
        LEFT JOIN Fanclub_Membership AS fm ON f.Fanclub_ID = fm.Fanclub_ID AND fm.Fan_ID = %s
    
    {where_clause}
    GROUP BY f.Fanclub_ID, f.Fanclub_Name, a.Artist_Name, fm.Fan_ID
    ORDER BY a.Artist_Name, f.Fanclub_Name
    '''

    query_parameters.insert(0, current_fan_id)
    fanclubs = execute_select_query(fanclub_query, tuple(query_parameters))

    return render_template(
        'fanclubs.html', 
        fanclubs=fanclubs,
        current_filter=current_filter,
        current_search=current_search,
        current_artist=current_artist, 
        artists=artists     
    )


# ============================================
#           USER MANAGEMENT (PLACEHOLDERS)
# ============================================
@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form.get('username')
        
        fan_query = '''
        SELECT Fan_ID, First_Name, Username, Email
        FROM Fan
        WHERE Username = %s OR Email = %s
        '''

        fan = execute_select_query(fan_query, (username_or_email, username_or_email))

        if fan:
            session['logged_in'] = True
            session['username'] = fan[0]['Username']
            session['fan_id'] = fan[0]['Fan_ID']
            
            flash(f'Login successful! Welcome back, {fan[0]["First_Name"]}.', 'success')
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

        fan_username_query = '''
        SELECT Fan_ID
        FROM Fan
        WHERE Username = %s
        '''

        fan_email_query = '''
        SELECT Fan_ID
        FROM Fan
        WHERE Email = %s
        '''

        fan_username = execute_select_query(fan_username_query, (username,))
        fan_email = execute_select_query(fan_email_query, (email,))
        
        if not all([first_name, last_name, username, email]):
            flash('All fields are required. Did you forget something?', 'error')
            return redirect(url_for('main_routes.register'))

        if fan_username:
            flash('An account with that username already exists. Try logging in!', 'error')
            return redirect(url_for('main_routes.register'))

        if fan_email:
            flash('An account with that email already exists. Try logging in!', 'error')
            return redirect(url_for('main_routes.register'))
            
        insert_fan_record = f'''
        INSERT INTO Fan (First_Name, Last_Name, Username, Email)
        VALUES (%s, %s, %s, %s)
        '''

        if execute_insert_query(insert_fan_record, (first_name, last_name, username, email)):
            flash(f'Welcome, {username}! You can now log in.', 'success')
            return redirect(url_for('main_routes.login'))
        else:
            flash('A server error occurred during registration. Please try again.', 'error')

    return render_template('register.html')


@main_routes.route('/profile')
def profile():
    current_fan_id = g.current_user.Fan_ID
    
    fan_query = '''
        SELECT Fan_ID, First_Name, Last_Name, Username, Email, Date_Joined
        FROM Fan
        WHERE Fan_ID = %s
        '''

    memberships_query = '''
    SELECT f.Fanclub_Name, fm.Date_Joined
    FROM Fanclub AS f
        JOIN Fanclub_Membership AS fm
            ON f.Fanclub_Id = fm.Fanclub_Id
            AND fm.Fan_Id = %s
    '''

    purchases_query = f'''
    SELECT e.Event_ID, e.Event_Name, t.Tier_Name, 
           tp.Fan_ID, tp.Ticket_ID, tp.Purchase_Date, 
           s.Seat_Row, s.Seat_Number, se.Section_Name
    FROM Event AS e
        JOIN Ticket_Purchase AS tp ON e.Event_Id = tp.Event_Id AND tp.Fan_Id = %s
        JOIN Ticket_Tier AS t ON t.Tier_Id = tp.Tier_Id 
        LEFT JOIN Seat AS s ON tp.Seat_Id = s.Seat_Id
        LEFT JOIN Section AS se ON s.Section_ID = se.Section_ID
    '''

    fan = execute_select_query(fan_query, (current_fan_id,))
    memberships = execute_select_query(memberships_query, (current_fan_id,))
    purchases = execute_select_query(purchases_query, (current_fan_id,))

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
    SELECT 
        Event_Record.*,
        (Event_Record.Total_Duration_In_Minutes / 60) AS Duration_Hours,
        (Event_Record.Total_Duration_In_Minutes % 60) AS Duration_Minutes,

        (   SELECT COUNT(*)
            FROM Ticket_Purchase tp
            WHERE tp.Event_ID = Event_Record.Event_ID
        )   AS Tickets_Sold,

        (   SELECT SUM(tt.Total_Quantity)
            FROM Ticket_Tier tt
            WHERE tt.Event_ID = Event_Record.Event_ID
        )   AS Max_Capacity
    FROM (
        SELECT 
            e.*,
            v.Venue_Name, v.City, v.Country, v.Is_Seated,
            DATEDIFF(e.Start_Date, CURDATE()) AS Days_Left,
            CASE
                WHEN e.End_Time >= e.Start_Time 
                THEN 
                    TIME_TO_SEC(TIMEDIFF(e.End_Time, e.Start_Time)) / 60
                ELSE 
                    TIME_TO_SEC(TIMEDIFF(ADDTIME(e.End_Time, '24:00:00'), e.Start_Time)) / 60
            END AS Total_Duration_In_Minutes
        FROM Event AS e JOIN Venue AS v ON e.Venue_ID = v.Venue_ID
        WHERE e.Event_ID = %s
    ) AS Event_Record
    '''

    # Error handling
    event_results = execute_select_query(event_query, (event_id,))
    if event_results:
        event = event_results[0]
    if not event:
        return redirect(url_for('main_routes.events'))

    tier_query = '''
    SELECT tt.*, 
           tt.Total_Quantity - COALESCE(tp.Tickets_Sold, 0) AS Tickets_Left
    FROM Ticket_Tier tt 
    LEFT JOIN (
        SELECT Tier_ID, COUNT(Ticket_ID) AS Tickets_Sold
        FROM Ticket_Purchase
        GROUP BY Tier_ID
    ) tp ON tt.Tier_ID = tp.Tier_ID
    WHERE Event_ID = %s
    '''
    ticket_tiers = execute_select_query(tier_query, (event_id,))  
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
        sections = execute_select_query(section_query, (tier['Tier_ID'],))

        if sections:
            tier_sections[tier['Tier_ID']] = sections
        else:
            tier_sections[tier['Tier_ID']] = []

    # Get purchase details
    if request.method == "POST":
        tier_id = request.form["ticket_tier"]
        seats_chosen = request.form.getlist("seat")
        values = []

        # Get non form values
        Fan_ID = session.get('fan_id')    
        Event_ID = event_id
        Tier_ID = tier_id
        Seat_ID = None
        
        if seats_chosen:
            for seat_id in seats_chosen:
                if seat_id == "":
                    seat_id = None   
                Seat_ID = seat_id  
                values.append((Fan_ID, Event_ID, Tier_ID, Seat_ID))  
        else:
            values.append((Fan_ID, Event_ID, Tier_ID, Seat_ID)) 

        insert_ticket_purchase = f'''
        INSERT INTO Ticket_Purchase (Fan_ID, Event_ID, Tier_ID, Seat_ID)
        VALUES (%s, %s, %s, %s)
        '''

        success = False
        for value in values:
            if execute_insert_query(insert_ticket_purchase, value):
                success = True
        
        if success:
            flash(f"Success! View your purchased tickets on your profile.", "success")
        else:
            flash(f"Error processing one or more purchases.", "error")

    return render_template(
        "buy_ticket.html", 
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
    per_page = request.args.get("per_page", 1000, type=int)

    seats_query = '''
    SELECT 
        s.Seat_ID, 
        s.Seat_Row, 
        s.Seat_Number, 
        
        CASE
            WHEN EXISTS (
                SELECT 1 FROM Ticket_Purchase AS tp
                WHERE tp.Seat_ID = s.Seat_ID AND tp.Event_ID = %s
            ) THEN 1
            ELSE 0
        END AS Is_Unavailable

    FROM Seat s
    WHERE s.Section_ID = %s
    ORDER BY s.Seat_ID
    LIMIT %s OFFSET %s
    '''

    # skips a number of records before returning results
    seats = []
    seats_results = execute_select_query(
        seats_query, (
            # For Derived Attribute - IsUnavailable
            event_id, 
            # For Pagination
            section_id, per_page, (page - 1) * per_page
        )
    )

    if seats_results:
        seats = seats_results

    total_seats_query = '''
    SELECT COUNT(Seat_ID) AS Total
    FROM Seat
    WHERE Section_ID = %s
    '''
    
    total_results = execute_select_query(total_seats_query, (section_id,))

    total_seats = 0
    if total_results:
        total_seats = total_results[0]['Total']

    # Use total_seats for your pagination calculations
    # 'total' for the pagination logic not len(seats)
    total = total_seats

    seat_list = [
        { "id": s['Seat_ID'], "seat_row": s['Seat_Row'], "seat_number": s['Seat_Number'],
          "is_unavailable": s['Is_Unavailable']
        }
        for s in seats
    ]

    return jsonify({
        "page": page,
        "per_page": per_page,
        "total": total,
        "seats": seat_list
    })

@main_routes.route('/ticket/<int:ticket_id>')
def view_ticket(ticket_id):
    ticket_query = '''
    SELECT tp.*, e.Event_Name, YEAR(e.Start_Date) AS Year, e.Start_Date, e.End_Date, 
           e.Start_Time, e.End_Time, v.Venue_Name,
           tt.Tier_Name, tt.Price, s.Seat_Row, s.Seat_Number, se.Section_Name
    FROM Ticket_Purchase tp
        JOIN Event e ON e.Event_ID = tp.Event_ID
        JOIN Ticket_Tier tt ON tt.Tier_ID = tp.Tier_ID
        JOIN Venue v ON v.Venue_ID = e.Venue_ID
        LEFT JOIN Seat s ON s.Seat_ID = tp.Seat_ID
        LEFT JOIN Section se ON se.Section_ID = s.Section_ID
    WHERE tp.Ticket_ID = %s
    '''

    tickets = execute_select_query(ticket_query, (ticket_id,))

    return render_template(
        "event_ticket.html",
        tickets=tickets
    )

# ============================================
#           Fanclub Subpages
# ============================================

@main_routes.route('/fanclubs/<int:fanclub_id>')
def fanclub_details(fanclub_id):

    current_fan_id = g.current_user.Fan_ID

    fanclub_query = '''
    SELECT f.*, a.Artist_Name, COUNT(fm.Fan_ID) AS Member_Count
    FROM Fanclub AS f 
        JOIN Artist AS a ON f.Artist_ID = a.Artist_ID
        LEFT JOIN Fanclub_Membership AS fm ON f.Fanclub_ID = fm.Fanclub_ID
    WHERE f.Fanclub_ID = %s
    GROUP BY f.Fanclub_ID
    '''

    is_member_query = '''
    SELECT Fan_Id
    FROM Fanclub_Membership
    WHERE Fanclub_ID = %s AND Fan_ID = %s
    '''

    merch_list_query = '''
    SELECT m.Merchandise_ID, m.Merchandise_Name, m.Merchandise_Price
    FROM Merchandise AS m 
        JOIN Fanclub AS f ON m.Fanclub_ID = f.Fanclub_ID
            AND f.Fanclub_ID = %s
    '''

    event_list_query = '''
    SELECT e.Event_ID, e.Event_Name, e.Start_Date, e.End_Date
    FROM Event AS e 
        JOIN Fanclub_Event AS fe ON e.Event_ID = fe.Event_ID
            AND fe.Fanclub_ID = %s
    '''

    event_merch_count_query = '''
    SELECT list1.Event_Count, list2.Merch_Count
    FROM (SELECT COUNT(*) AS Event_Count
            FROM Event AS e 
                JOIN Fanclub_Event AS fe ON e.Event_ID = fe.Event_ID
            WHERE fe.Fanclub_ID = %s) AS list1
        JOIN (SELECT COUNT(*) AS Merch_Count
                    FROM Merchandise AS m 
                        JOIN Fanclub AS f ON m.Fanclub_ID = f.Fanclub_ID
                    WHERE f.Fanclub_ID = %s) AS list2
    '''

    fanclub = execute_select_query(fanclub_query, (fanclub_id,))
    is_member = execute_select_query(is_member_query, (fanclub_id, current_fan_id))
    merch_list = execute_select_query(merch_list_query, (fanclub_id,))
    event_list = execute_select_query(event_list_query, (fanclub_id,))
    event_merch_count = execute_select_query(event_merch_count_query, (fanclub_id, fanclub_id))

    return render_template(
        'fanclub_details.html', 
        fanclub=fanclub,
        is_member=is_member,
        merch_list=merch_list,
        event_list=event_list,
        event_merch_count=event_merch_count)


@main_routes.route('/fanclubs/<int:fanclub_id>/members')
# @login_required # Ensure only logged-in users can view the list
def fanclub_members(fanclub_id):

    current_fan_id = g.current_user.Fan_ID

    is_member_query = '''
    SELECT Fan_Id
    FROM Fanclub_Membership
    WHERE Fanclub_ID = %s AND Fan_ID = %s
    '''

    fanclub_query = '''
    SELECT Fanclub_ID, Fanclub_Name
    FROM Fanclub
    WHERE Fanclub_ID = %s
    '''

    member_query = '''
    SELECT f.Username
    FROM Fanclub AS fc
        JOIN Fanclub_Membership AS fm ON fc.Fanclub_ID = fm.Fanclub_ID
        JOIN Fan AS f ON fm.Fan_ID = f.Fan_ID
    WHERE fc.Fanclub_ID = %s
    '''

    is_member = execute_select_query(is_member_query, (fanclub_id, current_fan_id))
    fanclub = execute_select_query(fanclub_query, (fanclub_id,))
    members = execute_select_query(member_query, (fanclub_id,))
    
    if not is_member[0]:
        flash(f"You must be a member of {fanclub[0].Fanclub_Name} to view this.", 'error')
        return redirect(url_for('main_routes.fanclub_details', fanclub_id=fanclub_id))
    
    return render_template(
        'fanclub_members.html', 
        fanclub=fanclub,
        is_member=is_member,
        members=members)


@main_routes.route('/fanclubs/<int:fanclub_id>/join', methods=['POST'])
def join_fanclub(fanclub_id):

    current_fan_id = g.current_user.Fan_ID

    insert_fanclub_membership_record = '''
    INSERT INTO Fanclub_Membership (Fan_ID, Fanclub_ID)
    VALUES (%s, %s)
    '''

    execute_insert_query(insert_fanclub_membership_record, (current_fan_id, fanclub_id))
    
    flash(f"You successfully joined this fanclub!", "success")
    return redirect(url_for('main_routes.fanclub_details', fanclub_id=fanclub_id))

@main_routes.route('/fanclubs/<int:fanclub_id>/leave', methods=['POST'])
def leave_fanclub(fanclub_id):

    current_fan_id = g.current_user.Fan_ID

    delete_fanclub_membership_record = '''
    DELETE FROM Fanclub_Membership
    WHERE Fan_ID = %s AND Fanclub_ID = %s
    '''

    execute_insert_query(delete_fanclub_membership_record, (current_fan_id, fanclub_id))
        
    flash(f"You successfully left this fanclub.", "success")
    return redirect(url_for('main_routes.fanclub_details', fanclub_id=fanclub_id))

@main_routes.route('/fanclub/<int:fanclub_id>/create-event', methods=['GET', 'POST'])
def create_fanclub_event(fanclub_id):

    fanclub_query = '''
    SELECT Fanclub_ID, Fanclub_Name, Artist_ID 
    FROM Fanclub
    WHERE Fanclub_ID = %s
    '''

    artist_query = '''
    SELECT Artist_Name
    FROM Artist
    WHERE Artist_ID = %s
    '''

    venue_query = '''
    SELECT Venue_ID, Venue_Name
    FROM Venue
    '''

    fanclub = execute_select_query(fanclub_query,  (fanclub_id,))
    artist = execute_select_query(artist_query, (fanclub[0]['Artist_ID'],))
    venues = execute_select_query(venue_query)
    
    if request.method == 'GET':        
        return render_template(
            'create_fanclub_event.html', 
            fanclub=fanclub, 
            artist=artist, 
            venues=venues
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


            insert_fanclub_membership_record = '''
            INSERT INTO Event (Event_Name, Event_Type, Venue_ID, Start_Date, End_Date, Start_Time, End_Time)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            '''

            event_query = '''
            SELECT Event_ID
            FROM Event
            WHERE Event_Name = %s
            '''

            insert_default_tier_record = '''
            INSERT INTO Ticket_Tier (Event_ID)
            VALUES (%s)
            '''

            insert_fanclub_event_record = '''
            INSERT INTO Fanclub_Event (Fanclub_ID, Event_ID)
            VALUES (%s, %s)
            '''

            execute_insert_query(insert_fanclub_membership_record, (
                event_name, 
                event_type,
                venue_id,
                start_date,
                end_date,
                start_time,
                end_time)
            )

            event = execute_select_query(event_query,  (event_name,))

            execute_insert_query(insert_default_tier_record, (event[0]['Event_ID'],))
            execute_insert_query(insert_fanclub_event_record, (fanclub_id, event[0]['Event_ID']))
            
            flash(f"Event '{event_name}' successfully created!", 'success')
            return redirect(url_for('main_routes.fanclub_details', fanclub_id=fanclub_id))
        
        except Exception as e:
            flash(f"An unexpected error occurred. {e}", 'error')

        artist_query = '''
        SELECT Artist_Name
        FROM Artist
        WHERE Artist_ID = %s
        '''

        venue_query = '''
        SELECT Venue_ID, Venue_Name
        FROM Venue
        '''

        artist = execute_select_query(artist_query, (fanclub[0]['Artist_ID'],))
        venues = execute_select_query(venue_query)

        return render_template('create_fanclub_event.html', 
            fanclub=fanclub, 
            artist=artist, 
            venues=venues
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

# =========================================================================
# MERCH SUBPAGES
# =========================================================================
@main_routes.route('/cart')
def cart():
    
    current_fan_id = session.get('fan_id')    

    active_cart_order = Order.query.filter_by(
            Fan_ID=current_fan_id, 
            Order_Status='Pending'
        ).first()

    cart_display_data = []
    cart_total = 0.0

    if active_cart_order:
        purchase_list = Purchase_List.query.filter_by(Order_ID=active_cart_order.Order_ID).all()
            
        for item in purchase_list:
            merch = item.merchandise 
            if merch:
                item_subtotal = float(merch.Merchandise_Price) * item.Quantity_Purchased
                cart_total += item_subtotal
                artist_name = merch.artist.Artist_Name if merch.artist else merch.fanclub.Fanclub_Name

                cart_display_data.append({
                    'id': merch.Merchandise_ID,
                    'name': merch.Merchandise_Name,
                    'artist' : artist_name,
                    'price': float(merch.Merchandise_Price),
                    'subtotal': item_subtotal,
                })

    context = {
        'cart_items': cart_display_data, 
        'cart_total': cart_total, 
        'item_count': len(cart_display_data) 
    }
        
    return render_template('cart.html', **context)


@main_routes.route('/cart/remove/<int:item_id>')
def remove_from_cart(item_id):
    
    current_fan_id = session.get('fan_id')
    
    active_cart_order = Order.query.filter_by(
        Fan_ID=current_fan_id, 
        Order_Status='Pending'
    ).first()
    
    if not active_cart_order:
        flash("Your cart is already empty.", 'info')
        return redirect(url_for('main_routes.cart'))

    item_to_remove = Purchase_List.query.filter_by(
        Order_ID=active_cart_order.Order_ID, 
        Merchandise_ID=item_id
    ).first()
    
    if item_to_remove:
        db.session.delete(item_to_remove)
        db.session.commit()
        flash("Item successfully removed from cart.", 'success')
    else:
        flash("That item wasn't in your cart.", 'warning')

    return redirect(url_for('main_routes.cart'))


@main_routes.route('/cart/clear')
def clear_cart():
    
    current_fan_id = session.get('fan_id')
    active_cart_order = Order.query.filter_by(
        Fan_ID=current_fan_id, 
        Order_Status='Pending'
    ).first()

    if active_cart_order:
        db.session.delete(active_cart_order)
        db.session.commit()
        flash("Your shopping cart has been completely emptied.", 'success')
    
    return redirect(url_for('main_routes.merchandise'))
    

@main_routes.route('/cart/add/<int:item_id>')
def add_to_cart(item_id):
    
    current_fan_id = session.get('fan_id')

    merchandise = Merchandise.query.filter_by(Merchandise_ID=item_id).first()
    if not merchandise or merchandise.Quantity_Stock <= 0:
        flash("🚫 Item is out of stock or not found!", 'danger')
        return redirect(url_for('main_routes.merchandise'))
    

    active_cart_order = Order.query.filter_by(
        Fan_ID=current_fan_id, 
        Order_Status='Pending'
    ).first()
    
    if not active_cart_order:
        active_cart_order = Order(Fan_ID=current_fan_id, Order_Status='Pending')
        db.session.add(active_cart_order)
        db.session.flush() 

    purchase_list_item = Purchase_List.query.filter_by(
        Order_ID=active_cart_order.Order_ID, 
        Merchandise_ID=item_id
    ).first()

    
    if purchase_list_item:
        purchase_list_item.Quantity_Purchased += 1
    else:
        purchase_list_item = Purchase_List(
            Order_ID=active_cart_order.Order_ID, 
            Merchandise_ID=item_id, 
            Quantity_Purchased=1
        )
        db.session.add(purchase_list_item)
        
    db.session.commit()
    
    flash(f"✅ '{merchandise.Merchandise_Name}' added to your cart!", 'success')
    return redirect(url_for('main_routes.cart'))

@main_routes.route('/checkout/place_order', methods=['POST']) 
def place_order():
    """
    Finalizes the order: Deducts stock, changes status to 'Paid'.
    This version uses the relationship attribute 'purchase_list'.
    """
    current_fan_id = session.get('fan_id')

    if not current_fan_id:
        flash("🚫 You must be logged in to place an order.", 'warning')
        return redirect(url_for('main_routes.login')) 


    active_cart_order = Order.query.filter_by(
        Fan_ID=current_fan_id, 
        Order_Status='Pending'
    ).first()


    if not active_cart_order or not active_cart_order.purchase_list:
        flash("🚫 Cart is empty or invalid.", 'danger')
        return redirect(url_for('main_routes.cart')) 

    try:
        for item in active_cart_order.purchase_list:
            merch = item.merchandise 
            
            if merch.Quantity_Stock >= item.Quantity_Purchased:
                merch.Quantity_Stock -= item.Quantity_Purchased
                db.session.add(merch)
            else:
                db.session.rollback() 
                flash(f"⚠️ Stock Error: '{merch.Merchandise_Name}' is sold out. Please update your cart.", 'danger')
                return redirect(url_for('main_routes.cart'))


        active_cart_order.Order_Status = 'Paid'
        active_cart_order.Order_Date = db.func.now() 
        db.session.add(active_cart_order)
        db.session.commit()
        
        flash(f"🎉 Order #{active_cart_order.Order_ID} placed successfully! Thank you!", 'success')
        
        return redirect(url_for('main_routes.merchandise'))
    
    except Exception as e:
        db.session.rollback()
        flash(f"❌ An internal error occurred. Order failed: {e}", 'danger')
        return redirect(url_for('main_routes.cart'))
