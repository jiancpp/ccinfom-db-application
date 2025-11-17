from flask import Blueprint, render_template, session, redirect, url_for, flash, g
from flask import render_template, request, redirect, url_for, jsonify
from collections import defaultdict

import datetime
import mysql.connector
from app.config import DB_HOST, DB_USER, DB_PASS, DB_NAME

# =========== REMOVE LATER ===================
from app.models import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from sqlalchemy import func, desc
# ============================================


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
    
    if g.get('current_user'):
        current_fan_id = g.current_user.Fan_ID

    search_term = request.args.get("artist-name", "").strip()
    filter_val = request.args.get("filter", "all") 

    query_parameters = []
    where_clauses = []

    artists_query_template = f'''
        SELECT 
            a.*,
            TIMESTAMPDIFF(DAY, a.Debut_Date, NOW()) AS Debut_Days,
            COUNT(DISTINCT af_all.Fan_ID) AS Num_Followers,
            MAX(CASE WHEN af_current.Fan_ID = %s THEN 1 ELSE 0 END) AS Is_Followed
        FROM 
            Artist AS a
        LEFT JOIN Artist_Follower AS af_all ON a.Artist_ID = af_all.Artist_ID
        LEFT JOIN Artist_Follower AS af_current ON a.Artist_ID = af_current.Artist_ID AND af_current.Fan_ID = %s
    '''

    query_parameters.append(current_fan_id)
    query_parameters.append(current_fan_id)

    if search_term:
        where_clauses.append("a.Artist_Name LIKE %s")
        query_parameters.append(f"%{search_term}%")

    if filter_val == 'followed':
        where_clauses.append("af_current.Fan_ID IS NOT NULL")
        
    elif filter_val == 'other':
        where_clauses.append("af_current.Fan_ID IS NULL")
    
    where_clause = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
    
    final_query = f'''
        {artists_query_template}
        {where_clause}
        GROUP BY a.Artist_ID, a.Artist_Name
        ORDER BY a.Artist_Name ASC
    '''

    artists = execute_select_query(final_query, tuple(query_parameters))

    return render_template(
        'artists.html', 
        artists=artists,
        current_filter=filter_val,
        current_search=search_term
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
def format_merch_row(row):
    """
    Converts a single SQL row (dictionary) into a readable dictionary 
    for the Jinja template, using column names as keys.
    """
    if not row:
        return {} 

    return {
        'id': row['Merchandise_ID'],
        'name': row['Merchandise_Name'],
        'description': row['Merchandise_Description'],
        'price': row['Merchandise_Price'],
        'stock': row['Quantity_Stock'],
        'artist_id': row['Artist_ID'],
        'fanclub_id': row['Fanclub_ID'],
        'event_id': row['Event_ID'],
        'artist_name': row['Artist_Name'],
        'fanclub_name': row['Fanclub_Name'],
        'event_name': row['Event_Name'] 
    }


@main_routes.route('/merchandise', methods=['GET'])
def merchandise():
    # --- 1. Get Filters and Display Mode ---
    artist_filter_id = request.args.get('artist_id', type=int)
    fanclub_filter_id = request.args.get('fanclub_id', type=int)
    search_query = request.args.get('search_query', '').strip()
    

    display_mode = request.args.get('filter', 'all') 
    
    raw_query = """
    SELECT
        M.Merchandise_ID, M.Merchandise_Name, M.Merchandise_Description, M.Merchandise_Price,
        M.Quantity_Stock, M.Artist_ID, M.Fanclub_ID, M.Event_ID,
        A.Artist_Name,
        F.Fanclub_Name,
        E.Event_Name
    FROM
        Merchandise M
    LEFT JOIN Artist A ON M.Artist_ID = A.Artist_ID
    LEFT JOIN Fanclub F ON M.Fanclub_ID = F.Fanclub_ID
    LEFT JOIN Event E ON M.Event_ID = E.Event_ID
    WHERE 1=1
    """
    
    parameters = []
    
    if artist_filter_id:
        raw_query += " AND M.Artist_ID = %s"
        parameters.append(artist_filter_id)

    if fanclub_filter_id:
        raw_query += " AND M.Fanclub_ID = %s"
        parameters.append(fanclub_filter_id)
        
    if search_query:
        raw_query += """ AND (
            LOWER(M.Merchandise_Name) LIKE %s 
            OR LOWER(M.Merchandise_Description) LIKE %s
        )"""
        
        search_param = f'%{search_query.lower()}%' 
        
        parameters.append(search_param)
        parameters.append(search_param)

    raw_query += " ORDER BY M.Merchandise_Name"

    
    if parameters:
        filtered_merch_rows = execute_select_query(raw_query, tuple(parameters))
    else:
        filtered_merch_rows = execute_select_query(raw_query)
        
    if filtered_merch_rows is not None:
        formatted_merchandise = [format_merch_row(row) for row in filtered_merch_rows]
    else:
        formatted_merchandise = []
        
    merch_by_artist = {}
    artist_names_map = {}
    artists_merch_data = [] 
    
    for item in formatted_merchandise:
        artist_id = item['artist_id'] 
        if artist_id is not None:
            merch_by_artist.setdefault(artist_id, []).append(item)
            artist_names_map[artist_id] = item['artist_name'] 
    
    for artist_id, merch_list in merch_by_artist.items():
        artists_merch_data.append({
            'name': artist_names_map[artist_id],
            'merchandise': merch_list
        })

    merch_by_fanclub = {}
    fanclub_names_map = {}
    fanclubs_merch_data = []
    
    for item in formatted_merchandise:
        fanclub_id = item['fanclub_id'] 
        if fanclub_id is not None:
            merch_by_fanclub.setdefault(fanclub_id, []).append(item)
            fanclub_names_map[fanclub_id] = item['fanclub_name']
            
    for fanclub_id, merch_list in merch_by_fanclub.items():
        fanclubs_merch_data.append({
            'name': fanclub_names_map[fanclub_id],
            'merchandise': merch_list
        })
    
    # single list for the 'All Merchandise' view
    all_merch_data = [{'name': 'All Merchandise', 'merchandise': formatted_merchandise}]
    
    # Query for All Artists/Fanclubs for Dropdowns
    raw_artists_data = execute_select_query("SELECT Artist_ID, Artist_Name FROM Artist ORDER BY Artist_Name") 
    all_artists_data = [{'id': row['Artist_ID'], 'name': row['Artist_Name']} for row in raw_artists_data]

    raw_fanclubs_data = execute_select_query("SELECT Fanclub_ID, Fanclub_Name FROM Fanclub ORDER BY Fanclub_Name")
    all_fanclubs_data = [{'id': row['Fanclub_ID'], 'name': row['Fanclub_Name']} for row in raw_fanclubs_data]
    
    return render_template(
        'merchandise.html', 
        artists_merch=artists_merch_data,
        fanclubs_merch=fanclubs_merch_data,
        all_artists=all_artists_data,
        all_fanclubs=all_fanclubs_data,
        search_query=search_query,
        artist_id=artist_filter_id,
        fanclub_id=fanclub_filter_id,
        filter=display_mode,
        all_merch=all_merch_data,
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
        conditions.append(search_condition)
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
        artist_condition = "a.Artist_Name LIKE %s"
        artist_pattern = f"%{current_artist}%"
        conditions.append(artist_condition)
        query_parameters.append(artist_pattern)


    # ----------------------------------------------------
    # BUILD QUERY 
    # ----------------------------------------------------

    where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""

    artist_query = '''
    SELECT Artist_Name 
    FROM Artist
    ORDER BY Artist_Name
    '''

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
    
    artists = execute_select_query(artist_query)
    fanclubs = execute_select_query(fanclub_query, tuple(query_parameters))

    return render_template(
        'fanclubs.html', 
        fanclubs=fanclubs,
        current_filter=current_filter,
        current_search=current_search,
        current_artist=current_artist, 
        artists=artists     
    )


@main_routes.route('/reports', methods=['GET'])
def reports():

    report_filter = request.args.get('filter', '') 
    selected_ticket_sales_year = request.args.get('year', type=int)
    selected_fanclub_contribution_year = request.args.get('year', type=int)
    selected_merch_sales_year = request.args.get('year', 2025, type=int)

    ticket_sales_data = ''
    sales_per_item = ''
    total_sales_data = ''
    artist_engagement_data = ''
    fanclub_contribution_data = ''

    # ----------------------------------------------------
    # TICKET SALES REPORT
    # ----------------------------------------------------
    if report_filter == 'ticket-sales-report':
        ticket_purchase_query = '''
        SELECT 
            RANK() OVER (ORDER BY COALESCE(tp.Ticket_Sales, 0) DESC) AS Ranking,
            e.Event_Name, 
            COALESCE(tp.Ticket_Sales, 0) AS Ticket_Sales, 
            COALESCE(tp.Earned_Revenue, 0) AS Earned_Revenue
        FROM Event e
            LEFT JOIN (
                SELECT tp.Event_ID, COUNT(tp.Ticket_ID) AS Ticket_Sales, SUM(tt.Price) AS Earned_Revenue
                FROM Ticket_Purchase tp
                    JOIN Ticket_Tier tt ON tt.Tier_ID = tp.Tier_ID
                GROUP BY tp.Event_ID
            ) tp ON e.Event_ID = tp.Event_ID
        WHERE YEAR(e.Start_Date) = %s
        ORDER BY tp.Ticket_Sales DESC, tp.Earned_Revenue DESC;
        '''
        ticket_sales_data = execute_select_query(ticket_purchase_query, (selected_ticket_sales_year,))
    

    # ----------------------------------------------------
    # MERCHANDISE SALES REPORT
    # ----------------------------------------------------
    if report_filter == 'merchandise-sales-report':
        
        # 1. Detailed Sales Ranking (Per Item, Per Creator)
    # Includes detailed metrics: Unsold Value, Merch Price, and is filtered by Year.
        sales_per_item_query = '''
            SELECT
                RANK() OVER (ORDER BY SUM(pl.Quantity_Purchased * m.Merchandise_Price) DESC) AS Ranking, 
                COALESCE(a.Artist_Name, f.Fanclub_Name) AS Creator_Name,
                m.Merchandise_Name AS Merchandise_Name,
                m.Merchandise_Price AS Merchandise_Price,
                m.Quantity_Stock AS Remaining_Stock,
                SUM(pl.Quantity_Purchased) AS Total_Quantity_Sold,
                SUM(pl.Quantity_Purchased * m.Merchandise_Price) AS Total_Sales_Revenue,
                
                COALESCE(AVG(M.Merchandise_Price), 0) AS Average_Sales_per_Item
            FROM
                Purchase_List pl
            JOIN
                `Order` o ON pl.Order_ID = o.Order_ID -- FIXED: Using backticks for the 'Order' table
            JOIN
                Merchandise m ON pl.Merchandise_ID = m.Merchandise_ID
            LEFT JOIN
                Artist a ON m.Artist_ID = a.Artist_ID
            LEFT JOIN
                Fanclub f ON m.Fanclub_ID = f.Fanclub_ID
            WHERE
                o.Order_Status IN ('Paid') 
                AND YEAR(o.Order_Date) = %s 
            GROUP BY
                m.Merchandise_ID, 
                m.Merchandise_Name,
                Creator_Name, 
                m.Quantity_Stock,
                m.Merchandise_Price
            ORDER BY
                Total_Sales_Revenue DESC;
        '''
        sales_per_item = execute_select_query(sales_per_item_query,(selected_merch_sales_year,))
        
        total_sales_sql = '''
            SELECT
                COALESCE(SUM(PL.Quantity_Purchased * M.Merchandise_Price), 0) AS Total_Sales_Revenue,
                COALESCE(SUM(PL.Quantity_Purchased), 0) AS Total_Quantity_Sold,
                
                -- Top Selling Item Subquery
                (
                    SELECT M_Top.Merchandise_Name
                    FROM Purchase_List PL_Top
                    JOIN Merchandise M_Top ON PL_Top.Merchandise_ID = M_Top.Merchandise_ID
                    JOIN `Order` O_Top ON PL_Top.Order_ID = O_Top.Order_ID
                    WHERE 
                        O_Top.Order_Status IN ('Paid') 
                        AND YEAR(O_Top.Order_Date) = %s -- Filter by Year only
                    GROUP BY M_Top.Merchandise_Name
                    ORDER BY SUM(PL_Top.Quantity_Purchased) DESC
                    LIMIT 1
                ) AS Top_Selling_Item
            
            FROM
                Purchase_List PL
            JOIN
                `Order` O ON PL.Order_ID = O.Order_ID
            JOIN
                Merchandise M ON PL.Merchandise_ID = M.Merchandise_ID
            WHERE
                O.Order_Status IN ('Paid') 
                AND YEAR(O.Order_Date) = %s; -- Filter by Year only
        '''
        # Pass YEAR TWICE (1 for the subquery, 1 for the main query)
        total_sales_data = execute_select_query( total_sales_sql, (selected_merch_sales_year, selected_merch_sales_year,))


    # ----------------------------------------------------
    # ARTIST ENGAGEMENT INDEX
    # ----------------------------------------------------
    if report_filter == 'artist-engagement-index':
        artist_engagement_data = ''


    # ----------------------------------------------------
    # FANCLUB CONTRIBUTION REPORT
    # ----------------------------------------------------
    if report_filter == 'fanclub-contribution-report':
        fanclub_contribution_query = '''
        SELECT
            RANK() OVER (ORDER BY (COALESCE(list1.Ticket_Sales, 0) + COALESCE(list2.Merch_Sales, 0)) DESC) AS Ranking,
            f.Fanclub_Name,
            COALESCE(list1.Ticket_Sales, 0) AS Total_Tickets,
            COALESCE(list2.Merch_Sales, 0) AS Total_Merchandise,
            (COALESCE(list1.Ticket_Sales, 0) + COALESCE(list2.Merch_Sales, 0)) AS Total_Sales
        FROM Fanclub AS f
        LEFT JOIN (
            SELECT fe.Fanclub_ID, SUM(t.Price) AS Ticket_Sales
            FROM Fanclub_Event AS fe
                LEFT JOIN Ticket_Purchase AS tp ON fe.Event_ID = tp.Event_ID
                LEFT JOIN Ticket_Tier AS t ON tp.Tier_ID = t.Tier_ID
            WHERE YEAR(tp.Purchase_Date) = %s
            GROUP BY fe.Fanclub_ID
        ) AS list1 ON f.Fanclub_ID = list1.Fanclub_ID
        LEFT JOIN (
            SELECT m.Fanclub_ID, SUM(m.Merchandise_Price * pl.Quantity_Purchased) AS Merch_Sales
            FROM Merchandise AS m
                LEFT JOIN Purchase_List AS pl ON m.Merchandise_ID = pl.Merchandise_ID
                LEFT JOIN `Order` AS o ON pl.Order_ID = o.Order_ID 
            WHERE YEAR(o.Order_Date) = %s
            GROUP BY m.Fanclub_ID
        ) AS list2 ON f.Fanclub_ID = list2.Fanclub_ID
        ORDER BY Total_Sales DESC
        '''
        fanclub_contribution_data = execute_select_query(fanclub_contribution_query, (selected_fanclub_contribution_year, selected_fanclub_contribution_year))

    
    return render_template(
        'reports.html',
        report_filter=report_filter, 
        ticket_sales_data=ticket_sales_data, 

        sales_per_item=sales_per_item,
        total_sales_data=total_sales_data,
        selected_merch_sales_year =selected_merch_sales_year,
        
        artist_engagement_data=artist_engagement_data,
        fanclub_contribution_data=fanclub_contribution_data,

        selected_ticket_sales_year=selected_ticket_sales_year,
        selected_fanclub_contribution_year=selected_fanclub_contribution_year
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
        SELECT *, DATEDIFF(CURDATE(), Date_Joined) AS Days_Since
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


@main_routes.route('/manager_portal')
def manager_portal():
    return render_template('manager_portal.html')


@main_routes.route('/manage_fans')
def manage_fans():
    # edit
    return render_template('manager_portal.html')


@main_routes.route('/manage_fanclubs')
def manage_fanclubs():
    # edit
    return render_template('manager_portal.html')


@main_routes.route('/manage_artists')
def manage_artists():
    # edit
    return render_template('manager_portal.html')


@main_routes.route('/manage_events')
def manage_events():
    # edit
    return render_template('manager_portal.html')


@main_routes.route('/manage_merchandise')
def manage_merchandise():
    # edit
    return render_template('manager_portal.html')


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
            v.Venue_Name, v.Location, lc.Country, v.Is_Seated,
            DATEDIFF(e.Start_Date, CURDATE()) AS Days_Left,
            CASE
                WHEN e.End_Time >= e.Start_Time 
                THEN 
                    TIME_TO_SEC(TIMEDIFF(e.End_Time, e.Start_Time)) / 60
                ELSE 
                    TIME_TO_SEC(TIMEDIFF(ADDTIME(e.End_Time, '24:00:00'), e.Start_Time)) / 60
            END AS Total_Duration_In_Minutes
        FROM Event AS e 
            JOIN Venue AS v ON e.Venue_ID = v.Venue_ID
            JOIN Location_Country AS lc ON lc.Location = v.Location
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
    SELECT  tt.*, 
            CASE
                WHEN tt.Total_Quantity IS NULL
                THEN 999999
                ELSE tt.Total_Quantity - COALESCE(tp.Tickets_Sold, 0)
            END AS Tickets_Left,
            
            CASE
                WHEN tt.Total_Quantity IS NOT NULL
                THEN 1 ELSE 0
            END AS Is_Limited_Tickets
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
        seats_chosen = request.form.getlist("seat")  # Reserved seats
        quantity = 0
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
            try:
                quantity = int(request.form.get('ticket-quantity', 0))
            except ValueError:
                quantity = 0
                
            for i in range(quantity):
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
            return redirect(url_for('main_routes.buy_ticket', event_id=event_id))
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
           e.Start_Time, e.End_Time, v.Venue_Name, v.Location,
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
    
    if not is_member:
        flash(f"You must be a member of {fanclub[0]['Fanclub_Name']} to view this.", 'error')
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
    artist_query = '''
        SELECT a.*,
               COUNT(af.Fan_ID) AS Num_Followers,
               TIMESTAMPDIFF(DAY, a.Debut_Date, CURDATE()) AS Debut_Days
        FROM Artist AS a
        LEFT JOIN Artist_Follower AS af ON a.Artist_ID = af.Artist_ID
        WHERE a.Artist_ID = %s
        GROUP BY a.Artist_ID
        '''
        
    manager_query = '''
        SELECT m.*
        FROM Manager AS m
        JOIN Artist AS a ON m.Manager_ID = a.Manager_ID
        WHERE a.Artist_ID = %s
        '''

    member_query = '''
        SELECT me.*,
            TIMESTAMPDIFF(YEAR, me.Birth_Date, CURDATE()) AS Age,
            me.Member_ID
        FROM Member AS me
        WHERE me.Artist_ID = %s
        ORDER BY me.Member_Name
        '''
    member_roles_query = '''
        SELECT mr.Member_ID, 
            r.Role_Name 
        FROM Member_Role AS mr
        JOIN Role AS r ON mr.Role_ID = r.Role_ID
        JOIN Member AS me ON mr.Member_ID = me.Member_ID
        WHERE me.Artist_ID = %s
        '''
    
    member_nationality_query = '''
        SELECT mn.Member_ID, 
            n.Nationality_Name 
        FROM Member_Nationality AS mn
        JOIN Nationality AS n ON mn.Nationality_ID = n.Nationality_ID
        JOIN Member AS me ON mn.Member_ID = me.Member_ID
        WHERE me.Artist_ID = %s
        '''

    artist_event_query = '''
        SELECT e.*
        FROM Event AS e
        JOIN Artist_Event AS ae ON e.Event_ID = ae.Event_ID
        WHERE ae.Artist_ID = %s AND e.Start_Date >= CURDATE()
        ORDER BY e.Start_Date ASC
        '''
    
    fanclub_query = '''
        SELECT f.*, 
               COUNT(m.Fan_ID) AS Member_Count
        FROM Fanclub AS f
        LEFT JOIN Fanclub_Membership AS m ON f.Fanclub_ID = m.Fanclub_ID
        WHERE f.Artist_ID = %s
        GROUP BY f.Fanclub_ID
        '''

    merch_query = '''
        SELECT * FROM Merchandise WHERE Artist_ID = %s
        '''
    
    follow_query = '''
        SELECT IF(COUNT(*) > 0, 1, 0) AS Is_Followed, Followed_Date
        FROM Artist_Follower
        WHERE Artist_ID = %s AND Fan_ID = %s
        '''
    
    event_fanclub_merch_count_query = '''
        SELECT list1.Event_Count AS Event, list2.Merch_Count AS Merch, list3.Fanclub_Count AS Fanclub, list4.Member_Count AS Member
        FROM (SELECT COUNT(*) AS Event_Count FROM Artist_Event AS ae
              WHERE ae.Artist_ID = %s) AS list1,
             (SELECT COUNT(*) AS Merch_Count FROM Merchandise AS m
              WHERE m.Artist_ID = %s) AS list2,
             (SELECT COUNT(*) AS Fanclub_Count FROM Fanclub AS f
              WHERE f.Artist_ID = %s) AS list3,
             (SELECT COUNT(*) AS Member_Count FROM Member AS me
              WHERE me.Artist_ID = %s) AS list4
    '''

    artist_result = execute_select_query(artist_query, (artist_id,))
    
    artist = artist_result[0]

    # artist['member'] = execute_select_query(member_query, (artist_id,))
    
    artist['events'] = execute_select_query(artist_event_query, (artist_id,))
    
    artist['merch'] = execute_select_query(merch_query, (artist_id,))

    artist['fanclub'] = execute_select_query(fanclub_query, (artist_id,))
    
    manager_list = execute_select_query(manager_query, (artist_id,))
    artist['manager'] = manager_list[0] if manager_list else None

    base_members_list = execute_select_query(member_query, (artist_id,))
    role_results = execute_select_query(member_roles_query, (artist_id,))
    nationality_results = execute_select_query(member_nationality_query, (artist_id,))

    member_roles_map = defaultdict(set) 
    for row in role_results:
        member_roles_map[row['Member_ID']].add(row['Role_Name'])

    member_nationality_map = defaultdict(set)
    for row in nationality_results:
        member_nationality_map[row['Member_ID']].add(row['Nationality_Name'])
        
    structured_members = []
    for member_data in base_members_list:
        member_id = member_data['Member_ID']
        
        roles_set = member_roles_map[member_id]
        member_data['Roles'] = sorted(list(roles_set))
        
        nationality_set = member_nationality_map[member_id]
        member_data['Nationalities'] = sorted(list(nationality_set))
        
        structured_members.append(member_data)

    artist['member'] = structured_members
    
    current_fan_id = g.current_user.Fan_ID
    
    followed_result = execute_select_query(follow_query, (artist_id, current_fan_id))
    Follow = followed_result[0] if followed_result else {'Is_Followed': 0, 'Followed_Date': None}
    Count = execute_select_query(event_fanclub_merch_count_query, (artist_id, artist_id, artist_id, artist_id))
    Count = Count[0] if Count else {'Event': 0, 'Merch': 0, 'Fanclub': 0, 'Member': 0}
    
    return render_template(
        'artist_details.html', 
        artist=artist,
        Follow=Follow,
        Count=Count
    )

@main_routes.route('/artists/toggle_follow/<int:artist_id>', methods=['POST'])
def toggle_follow(artist_id):

    current_fan_id = g.current_user.Fan_ID
    action = request.form.get('action') 

    artist_query = '''
        SELECT * FROM Artist WHERE Artist_ID = %s
        '''

    insert_artist_follower = '''
        INSERT INTO Artist_Follower (Fan_ID, Artist_ID, Followed_Date)
        VALUES (%s, %s, CURDATE())
        '''
    
    delete_artist_follower = '''
        DELETE FROM Artist_Follower
        WHERE Fan_ID = %s AND Artist_ID = %s
        '''

    artist = execute_select_query(artist_query, (artist_id,))
    
    if action == 'follow':
        execute_insert_query(insert_artist_follower, (current_fan_id, artist_id))
        flash(f"🎉 You are now following {artist[0]['Artist_Name']}! ", 'success')
        
    elif action == 'unfollow':
        execute_insert_query(delete_artist_follower, (current_fan_id, artist_id))
        flash(f"💔 You have unfollowed {artist[0]['Artist_Name']}.", 'error')

    return redirect(request.referrer or url_for('main_routes.artists'))
# =========================================================================
# MERCH SUBPAGES
# =========================================================================
@main_routes.route('/cart')
def cart():
    current_fan_id = session.get('fan_id')
    db_conn = None
    
    if not current_fan_id:
        cart_display_data = []
        cart_total = 0.0
        item_count = 0
    else:
        cart_display_data = []
        cart_total = 0.0
        total_units = 0
        
        try:
            db_conn = get_conn()
            cursor = db_conn.cursor(dictionary=True)
            
            sql_query = """
            SELECT
                M.Merchandise_ID AS id,
                M.Merchandise_Name AS name,
                COALESCE(A.Artist_Name, F.Fanclub_Name) AS artist,
                M.Merchandise_Price AS price,
                PL.Quantity_Purchased AS quantity,
                (M.Merchandise_Price * PL.Quantity_Purchased) AS subtotal
            FROM
                `Order` O
            JOIN
                Purchase_List PL ON O.Order_ID = PL.Order_ID
            JOIN
                Merchandise M ON PL.Merchandise_ID = M.Merchandise_ID
            LEFT JOIN
                Artist A ON M.Artist_ID = A.Artist_ID
            LEFT JOIN
                Fanclub F ON M.Fanclub_ID = F.Fanclub_ID
            WHERE
                O.Fan_ID = %s
                AND O.Order_Status = 'Pending';
            """
            
            cursor.execute(sql_query, (current_fan_id,))
            
            for item in cursor.fetchall():
                cart_display_data.append(item)
                cart_total += float(item['subtotal']) # Sum the calculated subtotal
                try:
                    total_units += int(item['quantity'])
                except (ValueError, TypeError):
                    total_units += 0

            cursor.close()

        except mysql.connector.Error as err:
            print(f"Database error in cart: {err}")
            flash("Error loading cart details.", 'danger')
        finally:
            if db_conn and db_conn.is_connected():
                db_conn.close()

    context = {
        'cart_items': cart_display_data, 
        'cart_total': cart_total, 
        'item_count': total_units
    }
    return render_template('cart.html', **context)


@main_routes.route('/cart/remove/<int:item_id>')
def remove_from_cart(item_id):
    current_fan_id = session.get('fan_id')
    db_conn = None
    
    if not current_fan_id:
        flash("Please log in to manage your cart.", 'warning')
        return redirect(url_for('main_routes.login'))

    try:
        db_conn = get_conn()
        cursor = db_conn.cursor()
        
        
        cursor.execute(
            """
            SELECT O.Order_ID, PL.Quantity_Purchased 
            FROM `Order` O
            JOIN Purchase_List PL ON O.Order_ID = PL.Order_ID
            WHERE O.Fan_ID = %s 
              AND O.Order_Status = 'Pending'
              AND PL.Merchandise_ID = %s;
            """, 
            (current_fan_id, item_id)
        )
        item_in_cart = cursor.fetchone()
        
        if not item_in_cart:
            flash("That item isn't in your cart.", 'warning')
            return redirect(url_for('main_routes.cart'))

        active_order_id = item_in_cart[0]
        try:
            current_quantity = int(item_in_cart[1])
        except (TypeError, ValueError):
            flash("Error processing item quantity.", 'danger')
            return redirect(url_for('main_routes.cart'))

        
        if current_quantity > 1:
            # If quantity is > 1, decrement by 1
            cursor.execute(
                """
                UPDATE Purchase_List 
                SET Quantity_Purchased = Quantity_Purchased - 1 
                WHERE Order_ID = %s AND Merchandise_ID = %s;
                """,
                (active_order_id, item_id)
            )
            flash("One unit of the item was removed from your cart.", 'success')
            
        else:
            cursor.execute(
                "DELETE FROM Purchase_List WHERE Order_ID = %s AND Merchandise_ID = %s;",
                (active_order_id, item_id)
            )
            flash("Item successfully removed from cart.", 'success')
            
        db_conn.commit()
        cursor.close()
            
    except mysql.connector.Error as err:
        if db_conn:
            db_conn.rollback()
        print(f"Database error on remove: {err}") 
        flash("An error occurred while removing the item.", 'danger')
        
    finally:
        if db_conn and db_conn.is_connected():
            db_conn.close()

    return redirect(url_for('main_routes.cart'))


@main_routes.route('/cart/clear')
def clear_cart():
    current_fan_id = session.get('fan_id')
    db_conn = None

    try:
        db_conn = get_conn()
        cursor = db_conn.cursor()
        
        cursor.execute(
            """
            UPDATE `Order` 
            SET Order_Status = 'Cancelled' 
            WHERE Fan_ID = %s AND Order_Status = 'Pending';
            """,
            (current_fan_id,)
        )

        if cursor.rowcount > 0:
            db_conn.commit()
            flash("Your current order has been cancelled, and the cart is emptied.", 'success')
        else:
            flash("No active order was found to cancel.", 'info')

        cursor.close()
            
    except mysql.connector.Error as err:
        if db_conn:
            db_conn.rollback()
        print(f"Database error on clear cart: {err}")
        flash("An error occurred while clearing the cart. Please try again.", 'danger')
        
    finally:
        if db_conn and db_conn.is_connected():
            db_conn.close()

    return redirect(url_for('main_routes.merchandise'))


@main_routes.route('/cart/add/<int:merchandise_id>')
def add_to_cart(merchandise_id):
    current_fan_id = session.get('fan_id')
    db_conn = None
    quantity_to_add = 1
    
    MAX_PURCHASE_LIMIT = 5 

    if not current_fan_id:
        flash("Please log in to add items to your cart.", 'warning')
        return redirect(url_for('main_routes.login'))

    try:
        db_conn = get_conn()
        cursor = db_conn.cursor()


        cursor.execute(
            "SELECT Order_ID FROM `Order` WHERE Fan_ID = %s AND Order_Status = 'Pending';",
            (current_fan_id,)
        )
        active_order = cursor.fetchone()
        
        if active_order:
            order_id = active_order[0]
        else:
            cursor.execute(
                "INSERT INTO `Order` (Fan_ID, Order_Status) VALUES (%s, 'Pending');",
                (current_fan_id,)
            )
            order_id = cursor.lastrowid
            
        cursor.execute(
            """
            SELECT SUM(PL.Quantity_Purchased) 
            FROM `Order` O
            JOIN Purchase_List PL ON O.Order_ID = PL.Order_ID
            WHERE O.Fan_ID = %s AND PL.Merchandise_ID = %s 
              AND O.Order_Status IN ('Paid', 'Shipped', 'Completed');
            """,
            (current_fan_id, merchandise_id)
        )
        
        existing_paid_qty = cursor.fetchone()[0] or 0 

        cursor.execute(
            "SELECT Quantity_Purchased FROM Purchase_List WHERE Order_ID = %s AND Merchandise_ID = %s;",
            (order_id, merchandise_id)
        )
        existing_cart_item = cursor.fetchone()
        current_cart_qty = existing_cart_item[0] if existing_cart_item else 0
        
        new_total_qty = existing_paid_qty + current_cart_qty + quantity_to_add
        
        if new_total_qty > MAX_PURCHASE_LIMIT:
            flash(
                f"🚫 Purchase limit reached! You have already bought {existing_paid_qty} units and have {current_cart_qty} in your cart. The maximum is {MAX_PURCHASE_LIMIT} per person.", 
                'danger'
            )
           
            db_conn.rollback() 
            cursor.close()
            return redirect(url_for('main_routes.merchandise'))
            
        
        if existing_cart_item:
            cursor.execute(
                "UPDATE Purchase_List SET Quantity_Purchased = Quantity_Purchased + %s WHERE Order_ID = %s AND Merchandise_ID = %s;",
                (quantity_to_add, order_id, merchandise_id)
            )
            flash("Item quantity updated in cart.", 'success')
        else:
            cursor.execute(
                "INSERT INTO Purchase_List (Order_ID, Merchandise_ID, Quantity_Purchased) VALUES (%s, %s, %s);",
                (order_id, merchandise_id, quantity_to_add)
            )
            flash("Item added to cart.", 'success')

        db_conn.commit()
        
    except mysql.connector.Error as err:
        if db_conn:
            db_conn.rollback()
        print(f"Database error while adding to cart: {err}")
        flash("Could not add item to cart due to a database error.", 'danger')
        
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if db_conn and db_conn.is_connected():
            db_conn.close()

    return redirect(url_for('main_routes.merchandise'))



@main_routes.route('/checkout/place_order', methods=['POST']) 
def place_order():
    current_fan_id = session.get('fan_id')

    db_conn = None
    
    try:
        db_conn = get_conn()
        db_conn.autocommit = False 
        cursor = db_conn.cursor()
        
        cursor.execute(
            """
            SELECT
                O.Order_ID,
                PL.Merchandise_ID,
                PL.Quantity_Purchased,
                M.Quantity_Stock,
                M.Merchandise_Name
            FROM
                `Order` O
            JOIN
                Purchase_List PL ON O.Order_ID = PL.Order_ID
            JOIN
                Merchandise M ON PL.Merchandise_ID = M.Merchandise_ID
            WHERE
                O.Fan_ID = %s AND O.Order_Status = 'Pending';
            """, 
            (current_fan_id,)
        )
        
        cart_details = cursor.fetchall()
        
        if not cart_details:
            flash("🚫 Cart is empty or invalid.", 'danger')
            cursor.close()
            return redirect(url_for('main_routes.cart')) 

        active_order_id = cart_details[0][0] # Order_ID is the first column

        for row in cart_details:
            merch_id = row[1]
            qty_purchased = row[2]
            qty_stock = row[3]
            merch_name = row[4]

            if qty_stock < qty_purchased:
                # Stock check failed, ROLLBACK and redirect
                db_conn.rollback() 
                flash(f"⚠️ Stock Error: '{merch_name}' is sold out. Please update your cart.", 'danger')
                cursor.close()
                return redirect(url_for('main_routes.cart'))

            # Deduct stock
            cursor.execute(
                """
                UPDATE Merchandise
                SET Quantity_Stock = Quantity_Stock - %s
                WHERE Merchandise_ID = %s;
                """,
                (qty_purchased, merch_id)
            )

        # 3. Finalize Order Status and Date
        cursor.execute(
            """
            UPDATE `Order`
            SET
                Order_Status = 'Paid',
                Order_Date = NOW() 
            WHERE
                Order_ID = %s;
            """,
            (active_order_id,)
        )
        
        db_conn.commit()
        
        flash(f"🎉 Order #{active_order_id} placed successfully! Thank you!", 'success')
        
        return redirect(url_for('main_routes.merchandise'))
    
    except mysql.connector.Error as err:
        # Rollback on ANY database error
        if db_conn:
            db_conn.rollback()
        
        flash(f"❌ An internal database error occurred. Order failed. Error: {err}", 'danger')
        return redirect(url_for('main_routes.cart'))
        
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if db_conn and db_conn.is_connected():
            db_conn.close()
