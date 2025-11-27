from flask import Blueprint, render_template, session, redirect, url_for, flash, g
from flask import render_template, request, redirect, url_for, jsonify
from collections import defaultdict

import datetime
import re
import mysql.connector

from .db_utils import execute_select_query, execute_insert_query, get_conn, get_updated_value, execute_modified_insert, execute_select_one_query

main_routes = Blueprint('main_routes', __name__)

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
            fan_ID = g.current_user['Fan_ID'] if g.current_user else None 
            artist_query = '''
                SELECT a.*, 
                       COUNT(af_count.Fan_ID) AS Num_Followers
                FROM Artist AS a
                JOIN Artist_Follower AS af ON a.Artist_ID = af.Artist_ID
                LEFT JOIN Artist_Follower AS af_count ON a.Artist_ID = af_count.Artist_ID 
                WHERE af.Fan_ID = %s
                GROUP BY a.Artist_ID, a.Artist_Name
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
        current_fan_id = g.current_user['Fan_ID'] if g.current_user else None

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
        'event_names': row.get('Event_Names', 'N/A'), 
        'artist_name': row['Artist_Name'],
        'fanclub_name': row['Fanclub_Name'],
    }


@main_routes.route('/merchandise', methods=['GET'])
def merchandise():
    artist_filter_id = request.args.get('artist_id', type=int)
    fanclub_filter_id = request.args.get('fanclub_id', type=int)
    search_query = request.args.get('search_query', '').strip()
    
    display_mode = request.args.get('filter', 'all') 
    
    
    raw_query = """
    SELECT
        M.Merchandise_ID, M.Merchandise_Name, M.Merchandise_Description, M.Merchandise_Price,
        M.Quantity_Stock, M.Artist_ID, M.Fanclub_ID,
        A.Artist_Name,
        F.Fanclub_Name,
        -- Aggregate all linked event names into a single string
        GROUP_CONCAT(DISTINCT E.Event_Name SEPARATOR ', ') AS Event_Names 
    FROM
        Merchandise M
    LEFT JOIN Artist A ON M.Artist_ID = A.Artist_ID
    LEFT JOIN Fanclub F ON M.Fanclub_ID = F.Fanclub_ID
    LEFT JOIN Merchandise_Event ME ON M.Merchandise_ID = ME.Merchandise_ID
    LEFT JOIN Event E ON ME.Event_ID = E.Event_ID
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
        
    raw_query += """
    GROUP BY
        M.Merchandise_ID, M.Merchandise_Name, M.Merchandise_Description, M.Merchandise_Price,
        M.Quantity_Stock, M.Artist_ID, M.Fanclub_ID, A.Artist_Name, F.Fanclub_Name
    ORDER BY M.Merchandise_Name
    """
    
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
    

    all_merch_data = [{'name': 'All Merchandise', 'merchandise': formatted_merchandise}]
    
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
    if not g.get('current_user'):
        flash("You must be logged in to view fan clubs", "error")
        return redirect(url_for('main_routes.login'))

    # ----------------------------------------------------
    # SETUP & INPUTS
    # ---------------------------------------------------- 
    conditions = []
    query_parameters = []

    current_fan_id = g.current_user['Fan_ID'] if g.current_user else None
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
    selected_year = request.args.get('year', type=int)
    default_year = 2025 

    selected_ticket_sales_year = selected_year if selected_year is not None else default_year
    selected_fanclub_contribution_year = selected_year if selected_year is not None else default_year
    selected_merch_sales_year = selected_year if selected_year is not None else default_year 
    selected_artist_contribution_year = selected_year if selected_year is not None else default_year

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
        artist_engagement_data = '''
            SELECT
                Metrics.Artist_Name AS Artist_Name,
                DENSE_RANK() OVER (ORDER BY Metrics.AEI_Score DESC) AS AEI_Rank,
                Metrics.AEI_Score AS AEI_Score,
                Metrics.New_Followers_Count AS New_Followers_Count,
                Metrics.New_Members_Count AS New_Members_Count,
                Metrics.Ticket_Revenue_Amount AS Ticket_Revenue_Amount,
                Metrics.Merchandise_Revenue_Amount AS Merchandise_Revenue_Amount
            FROM (
                SELECT
                    A.Artist_Name,
                    A.Artist_ID,
                    COALESCE(AF_Year.New_Followers, 0) AS New_Followers_Count,
                    COALESCE(FM_Year.New_Members, 0) AS New_Members_Count,
                    COALESCE(TP_Year.Ticket_Revenue, 0) AS Ticket_Revenue_Amount,
                    COALESCE(MR_Year.Merchandise_Revenue, 0) AS Merchandise_Revenue_Amount,
                    -- Calculate the raw AEI Score
                    (
                        COALESCE(AF_Year.New_Followers, 0) * 0.15
                        + COALESCE(FM_Year.New_Members, 0) * 0.25
                        + COALESCE(TP_Year.Ticket_Revenue, 0) * 0.30
                        + COALESCE(MR_Year.Merchandise_Revenue, 0) * 0.30
                    ) AS AEI_Score
                    
                FROM Artist A
                        
                LEFT JOIN (
                    SELECT Artist_ID, COUNT(Fan_ID) AS New_Followers
                    FROM Artist_Follower
                    WHERE YEAR(Followed_Date) = %s
                    GROUP BY Artist_ID
                ) AS AF_Year ON A.Artist_ID = AF_Year.Artist_ID
                        
                LEFT JOIN (
                    SELECT FC.Artist_ID, COUNT(FM.Fan_ID) AS New_Members
                    FROM Fanclub_Membership FM
                    JOIN Fanclub FC ON FM.Fanclub_ID = FC.Fanclub_ID
                    WHERE YEAR(FM.Date_Joined) = %s 
                    GROUP BY FC.Artist_ID
                ) AS FM_Year ON A.Artist_ID = FM_Year.Artist_ID

                LEFT JOIN (
                    SELECT AE.Artist_ID, SUM(TT.Price) AS Ticket_Revenue
                    FROM Ticket_Purchase TP
                    JOIN Ticket_Tier TT ON TP.Tier_ID = TT.Tier_ID
                    JOIN Artist_Event AE ON TP.Event_ID = AE.Event_ID
                    WHERE YEAR(TP.Purchase_Date) = %s 
                    GROUP BY AE.Artist_ID
                ) AS TP_Year ON A.Artist_ID = TP_Year.Artist_ID

                LEFT JOIN (
                    SELECT M.Artist_ID, SUM(PL.Quantity_Purchased * M.Merchandise_Price) AS Merchandise_Revenue
                    FROM Purchase_List PL
                    JOIN Merchandise M ON PL.Merchandise_ID = M.Merchandise_ID
                    JOIN `Order` O ON PL.Order_ID = O.Order_ID
                    WHERE O.Order_Status = 'Paid'
                    AND YEAR(O.Order_Date) = %s 
                    AND M.Artist_ID IS NOT NULL 
                    GROUP BY M.Artist_ID
                ) AS MR_Year ON A.Artist_ID = MR_Year.Artist_ID
            ) AS Metrics
        ORDER BY
            AEI_Rank ASC;
        '''
        artist_engagement_data = execute_select_query(artist_engagement_data, (selected_artist_contribution_year, selected_artist_contribution_year, selected_artist_contribution_year, selected_artist_contribution_year))
    # ----------------------------------------------------
    # FANCLUB CONTRIBUTION REPORT
    # ----------------------------------------------------
    if report_filter == 'fanclub-contribution-report':
        fanclub_contribution_query = '''
        SELECT
            RANK() OVER (ORDER BY (COALESCE(list1.Ticket_Sales, 0) + COALESCE(list2.Merch_Sales, 0) + 
            COALESCE(list3.Member_Ticket_Purchase, 0) + COALESCE(list4.Member_Merch_Purchase, 0)) DESC) AS Ranking,
            f.Fanclub_Name,
            COALESCE(list1.Ticket_Sales, 0) AS Total_Tickets,
            COALESCE(list2.Merch_Sales, 0) AS Total_Merchandise,
            COALESCE(list3.Member_Ticket_Purchase, 0) AS Total_Member_Tickets,
            COALESCE(list4.Member_Merch_Purchase, 0) AS Total_Member_Merchandise,
            (COALESCE(list1.Ticket_Sales, 0) + COALESCE(list2.Merch_Sales, 0) + 
            COALESCE(list3.Member_Ticket_Purchase, 0) + COALESCE(list4.Member_Merch_Purchase, 0)) AS Total_Sales
        FROM Fanclub AS f
        LEFT JOIN (
            SELECT fe.Fanclub_ID, SUM(t.Price) AS Ticket_Sales
            FROM Fanclub_Event AS fe
                LEFT JOIN Ticket_Tier AS t ON fe.Event_ID = t.Event_ID
                LEFT JOIN Ticket_Purchase AS tp ON t.Tier_ID = tp.Tier_ID
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
        LEFT JOIN (
			SELECT fm.Fanclub_ID, SUM(t.Price) AS Member_Ticket_Purchase
            FROM Fanclub_Membership AS fm
				LEFT JOIN Ticket_Purchase AS tp ON fm.Fan_ID = tp.Fan_ID
                LEFT JOIN Ticket_Tier AS t ON tp.Tier_ID = t.Tier_ID
                LEFT JOIN Artist_Event AS ae ON t.Event_ID = ae.Event_ID
                LEFT JOIN Fanclub AS fc ON fm.Fanclub_ID = fc.Fanclub_ID
            WHERE YEAR(tp.Purchase_Date) = %s AND ae.Artist_ID = fc.Artist_ID
            GROUP BY fm.Fanclub_ID
		) AS list3 ON f.Fanclub_ID = list3.Fanclub_ID
        LEFT JOIN (
            SELECT fm.Fanclub_ID, SUM(m.Merchandise_Price * pl.Quantity_Purchased) AS Member_Merch_Purchase
            FROM Fanclub_Membership AS fm
                LEFT JOIN `Order` AS o ON fm.Fan_ID = o.Fan_ID
                LEFT JOIN Purchase_List AS pl ON o.Order_ID = pl.Order_ID
                LEFT JOIN Merchandise AS m ON pl.Merchandise_ID = m.Merchandise_ID
            WHERE YEAR(o.Order_Date) = %s
            GROUP BY fm.Fanclub_ID
        ) AS list4 ON f.Fanclub_ID = list4.Fanclub_ID
        ORDER BY Total_Sales DESC;
        '''
        fanclub_contribution_data = execute_select_query(fanclub_contribution_query, (selected_fanclub_contribution_year, 
                                                                                      selected_fanclub_contribution_year,
                                                                                      selected_fanclub_contribution_year, 
                                                                                      selected_fanclub_contribution_year))

    
    return render_template(
        'reports.html',
        report_filter=report_filter, 
        ticket_sales_data=ticket_sales_data, 

        sales_per_item=sales_per_item,
        total_sales_data=total_sales_data,
        
        artist_engagement_data=artist_engagement_data,
        fanclub_contribution_data=fanclub_contribution_data,

        selected_ticket_sales_year=selected_ticket_sales_year,
        selected_fanclub_contribution_year=selected_fanclub_contribution_year,
        selected_artist_contribution_year=selected_artist_contribution_year,
        selected_merch_sales_year =selected_merch_sales_year
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
    current_fan_id = g.current_user['Fan_ID'] if g.current_user else None
    
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

@main_routes.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():

    current_fan_id = g.current_user['Fan_ID']
    
    fan_query = '''
        SELECT *
        FROM Fan
        WHERE Fan_ID = %s
        '''
        
    fan = execute_select_query(fan_query, (current_fan_id,))

    if not fan:
        flash('Error loading profile data.', 'error')
        return redirect(url_for('main_routes.profile'))
    
    if request.method == 'POST':
        current_fan_id = g.current_user['Fan_ID']

        first_name = get_updated_value('first_name', fan[0]['First_Name'])
        last_name = get_updated_value('last_name', fan[0]['Last_Name'])
        username = get_updated_value('username', fan[0]['Username'])
        email = get_updated_value('email', fan[0]['Email'])

        fan_username_query = '''
        SELECT Fan_ID
        FROM Fan
        WHERE Username = %s AND Fan_ID != %s
        '''
        fan_username = execute_select_query(fan_username_query, (username, current_fan_id))

        if fan_username:
            flash(f'The username "{username}" is already taken.', 'error')
            return render_template('edit_profile.html', fan=fan)

        fan_email_query = '''
        SELECT Fan_ID
        FROM Fan
        WHERE Email = %s AND Fan_ID != %s
        '''
        fan_email = execute_select_query(fan_email_query, (email, current_fan_id))

        if fan_email:
            flash(f'The email "{email}" is already registered.', 'error')
            return render_template('edit_profile.html', fan=fan)
            
        update_fan_record = '''
        UPDATE Fan
        SET First_Name = %s,
            Last_Name = %s,
            Username = %s,
            Email = %s
        WHERE Fan_ID = %s
        '''

        if execute_insert_query(update_fan_record, (first_name, last_name, username, email, current_fan_id)):
            session['username'] = username
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('main_routes.profile'))
        else:
            flash('A server error occurred.', 'error')

    return render_template('edit_profile.html', fan=fan)

@main_routes.route('/delete_account', methods=['POST'])
def delete_account():
    current_fan_id = g.current_user['Fan_ID']

    session.pop('fan_id', None)
    session.pop('username', None)
    session.pop('logged_in', None)

    delete_fanclub_membership_record = '''
    DELETE FROM Fan
    WHERE Fan_ID = %s
    '''

    execute_insert_query(delete_fanclub_membership_record, (current_fan_id, ))

    flash('Account deleted successfully.', 'success')
    return redirect(url_for('main_routes.index'))

@main_routes.route('/manager_portal')
def manager_portal():
    return render_template('manager_portal.html')


@main_routes.route('/manage_fanclubs')
def manage_fanclubs():
    query = '''
    SELECT 
        f.*, 
        a.Artist_Name
    FROM Fanclub AS f 
        JOIN Artist AS a ON f.Artist_ID = a.Artist_ID
    '''

    fanclubs = execute_select_query(query)

    return render_template(
        'manage_fanclubs.html', 
        fanclubs=fanclubs
    )


@main_routes.route('/manage_fanclubs/add_fanclub', methods=['GET', 'POST'])
def add_fanclub():
    artist_query = '''
    SELECT Artist_ID, Artist_Name
    FROM Artist
    ORDER BY Artist_Name
    '''
    artists = execute_select_query(artist_query)

    if request.method == 'POST':
        try:
            fanclub_name = request.form.get('fanclub_name')
            artist_id = request.form.get('artist_id')
            
            if not fanclub_name or not artist_id:
                flash("Fanclub Name and Associated Artist are required.", 'error')
                return redirect(request.url)
            
            check_name_query = '''
            SELECT Fanclub_ID FROM Fanclub WHERE Fanclub_Name = %s
            '''
            existing_fanclub = execute_select_query(check_name_query, (fanclub_name,))

            if existing_fanclub:
                flash(f"A fanclub named '{fanclub_name}' already exists. Please choose a unique name.", 'error')
                return render_template('add_fanclub.html', artists=artists)

            insert_fanclub_record = '''
            INSERT INTO Fanclub (Fanclub_Name, Artist_ID)
            VALUES (%s, %s)
            '''
            
            execute_insert_query(insert_fanclub_record, (
                fanclub_name, 
                artist_id)
            )

            flash(f"Fanclub '{fanclub_name}' successfully created!", 'success')
            return redirect(url_for('main_routes.manage_fanclubs'))
        
        except Exception as e:
            flash(f"An unexpected error occurred while adding the fanclub: {e}", 'error')
            return render_template('add_fanclub.html', artists=artists)

    return render_template('add_fanclub.html', artists=artists)


@main_routes.route('/manage_fanclubs/<int:fanclub_id>/edit_fanclub', methods=['GET', 'POST'])
def edit_fanclub(fanclub_id):
    fanclub_query = '''
    SELECT Fanclub_ID, Fanclub_Name, Artist_ID 
    FROM Fanclub
    WHERE Fanclub_ID = %s
    '''
    artist_query = '''
    SELECT Artist_ID, Artist_Name
    FROM Artist
    ORDER BY Artist_Name
    '''
    
    fanclub_data = execute_select_query(fanclub_query, (fanclub_id,))  
    fanclub = fanclub_data[0]
    artists = execute_select_query(artist_query)

    if request.method == 'POST':
        try:
            new_name = request.form.get('fanclub_name')
            new_artist_id = request.form.get('artist_id')
            
            if not new_name or not new_artist_id:
                flash("Fanclub Name and Associated Artist are required.", 'error')
                return render_template('edit_fanclub.html', fanclub=fanclub, artists=artists)

            if new_name != fanclub['Fanclub_Name']:
                check_name_query = '''
                SELECT Fanclub_ID FROM Fanclub WHERE Fanclub_Name = %s
                '''
                existing_fanclub = execute_select_query(check_name_query, (new_name,))

                if existing_fanclub:
                    flash(f"A fanclub named '{new_name}' already exists. Please choose a unique name.", 'error')
                    return render_template('edit_fanclub.html', fanclub=fanclub, artists=artists)

            update_fanclub_query = '''
            UPDATE Fanclub
            SET Fanclub_Name = %s, Artist_ID = %s
            WHERE Fanclub_ID = %s
            '''
            
            execute_insert_query(update_fanclub_query, (
                new_name, 
                new_artist_id,
                fanclub_id)
            )

            flash(f"Fanclub '{new_name}' updated successfully!", 'success')
            return redirect(url_for('main_routes.manage_fanclubs'))
        
        except Exception as e:
            flash(f"An unexpected error occurred while updating the fanclub: {e}", 'error')
            return render_template('edit_fanclub.html', fanclub=fanclub, artists=artists)

    return render_template('edit_fanclub.html', fanclub=fanclub, artists=artists)


@main_routes.route('/manage_fanclubs/<int:fanclub_id>/delete_fanclub', methods=['POST'])
def delete_fanclub(fanclub_id):
    fanclub_name_query = "SELECT Fanclub_Name FROM Fanclub WHERE Fanclub_ID = %s"
    fanclub_data = execute_select_query(fanclub_name_query, (fanclub_id,))
    
    if not fanclub_data:
        flash("Fanclub not found.", 'error')
        return redirect(url_for('main_routes.manage_fanclubs'))

    fanclub_name = fanclub_data[0]['Fanclub_Name']
    
    try:
        delete_query = '''
        DELETE FROM Fanclub
        WHERE Fanclub_ID = %s
        '''
    
        execute_insert_query(delete_query, (fanclub_id,))

        flash(f"Fanclub '{fanclub_name}' successfully deleted.", 'success')
        return redirect(url_for('main_routes.manage_fanclubs'))
        
    except Exception as e:
        flash(f"Error deleting fanclub '{fanclub_name}'. It may be associated with existing records (Events, etc.). Error: {e}", 'error')
        return redirect(url_for('main_routes.manage_fanclubs'))


@main_routes.route('/manage_artists')
def manage_artists():
    query = """
        SELECT
            A.Artist_ID AS Artist_ID,
            A.Artist_Name AS Artist_Name,
            A.Activity_Status AS Activity_Status,
            A.Debut_Date AS Debut_Date,
            M.Manager_Name AS Manager_Name
        FROM
            Artist A
        LEFT JOIN
            Manager M ON A.Manager_ID = M.Manager_ID
        GROUP BY
            A.Artist_ID, A.Artist_Name, A.Activity_Status, A.Debut_Date, M.Manager_Name, M.Agency
        ORDER BY 
            A.Artist_ID;
        """
        
    artists = execute_select_query(query)
        
    return render_template('manage_artists.html', artists=artists)

@main_routes.route('/manage_artists/<int:artist_id>/delete_artist', methods=['POST'])
def delete_artist(artist_id):
    artist_name_query = "SELECT Artist_Name FROM Artist WHERE Artist_ID = %s"
    artist_data = execute_select_query(artist_name_query, (artist_id,))
    
    if not artist_data:
        flash("Artist not found.", 'error')
        return redirect(url_for('main_routes.manage_artists'))

    artist_name = artist_data[0]['Artist_Name']
    
    try:
        delete_query = '''
        DELETE FROM Artist
        WHERE Artist_ID = %s
        '''
    
        execute_insert_query(delete_query, (artist_id,))

        flash(f"Artist '{artist_name}' successfully deleted.", 'success')
        return redirect(url_for('main_routes.manage_artists'))
        
    except Exception as e:
        flash(f"Error deleting artist '{artist_name}'. It may be associated with existing records (Events, etc.). Error: {e}", 'error')
        return redirect(url_for('main_routes.manage_artists'))

@main_routes.route('/manage_artist/add_artist_info', methods=["GET","POST"])
def add_artist_info():
    role_query = '''
    SELECT Role_Name
    FROM REF_Role
    ORDER BY Role_Name
    '''
    nationality_query = '''
    SELECT Nationality_Name
    FROM REF_Nationality
    ORDER BY Nationality_Name
    '''

    dbroles = execute_select_query(role_query)
    dbnationalities = execute_select_query(nationality_query)

    roles = [
        {'value': str(row['Role_Name']), 'text': str(row['Role_Name'])}
        for row in dbroles if 'Role_Name' in row
    ]

    nationalities = [
        {'value': str(row['Nationality_Name']), 'text': str(row['Nationality_Name'])}
        for row in dbnationalities if 'Nationality_Name' in row
    ]

    return render_template(
        'add_artist_info.html',
        roles=roles,
        nationalities=nationalities
    )

@main_routes.route('/manage_artist/add_artist_info/add_artist', methods=["GET","POST"])
def add_artist():
    if request.method == 'POST':
        
        artist_data = {
            'artist_name': request.form.get('artist_name'),
            'debut_date': request.form.get('debut_date'),
            'activity_status': request.form.get('activity_status'),
            'agency': request.form.get('agency'),
            'manager_name': request.form.get('new_manager_name'),
            'manager_phone': request.form.get('new_manager_phone'),
            'manager_email': request.form.get('new_manager_email'),
        }
        
        member_data_map = {} 
        final_members_list = []
        
        for key, value in request.form.items():
            if key.startswith('members['):
                match = re.search(r'members\[(\d+)\]\[(\w+)\]', key)
                
                if match:
                    index = int(match.group(1))
                    field_name = match.group(2)
                    
                    if index not in member_data_map:
                        member_data_map[index] = {}
                    
                    member_data_map[index][field_name] = value

        for index in sorted(member_data_map.keys()):
            member_dict = member_data_map[index]
            role_key = f'members[{index}][role]'
            nationality_key = f'members[{index}][nationality]'
            
            member_dict['role'] = request.form.getlist(role_key)
            member_dict['nationality'] = request.form.getlist(nationality_key)
            
            final_members_list.append(member_dict)
        
        conn = get_conn() 
        cursor = conn.cursor()

        try:
            if (artist_data['manager_name']): 
                manager_insert_sql = '''
                INSERT INTO Manager (Manager_Name, Agency, Contact_Num, Contact_Email)
                VALUES (%s, %s, %s, %s)
                '''
                cursor.execute(manager_insert_sql, (
                    artist_data['manager_name'], 
                    artist_data['agency'], 
                    artist_data['manager_phone'], 
                    artist_data['manager_email']
                ))

                manager_id = cursor.lastrowid
                if not manager_id:
                    raise Exception("Failed to retrieve Manager ID after insertion.")
            else:
                manager_id = None

            artist_insert_sql = '''
            INSERT INTO Artist (Artist_Name, Debut_Date, Activity_Status, Manager_ID)
            VALUES (%s, %s, %s, %s)
            '''
            cursor.execute(artist_insert_sql, (
                artist_data['artist_name'],
                artist_data['debut_date'],
                artist_data['activity_status'],
                manager_id
            ))
            
            artist_id = cursor.lastrowid
            if not artist_id:
                raise Exception("Failed to retrieve Artist ID after insertion.")

            for member_data in final_members_list:
                
            
                member_insert_sql = '''
                -- NOTE: The SQL MUST include Artist_ID as the first parameter
                INSERT INTO Member (Artist_ID, Member_Name, Birth_Date, Activity_Status)
                VALUES (%s, %s, %s, %s)
                '''
                cursor.execute(member_insert_sql, (
                    artist_id,                  
                    member_data['name'],          
                    member_data.get('artist_name'), 
                    member_data['activity_status']
                ))

             
                member_id = cursor.lastrowid
                if not member_id:
                    raise Exception(f"Failed to retrieve Member ID after insertion for member: {member_data['name']}")

             
                for nation_name in member_data.get('nationality', []):
               
                    nationality_lookup_sql = "SELECT Nationality_ID FROM REF_Nationality WHERE Nationality_Name = %s"
                    cursor.execute(nationality_lookup_sql, (nation_name,))
                    
                    result = cursor.fetchone()
                    
                    if result:
                        nationality_id = result[0]
                    else:
                        raise ValueError(f"Selected nationality '{nation_name}' not found in database.")
                    
  
                    member_nation_link_sql = '''
                    INSERT INTO LINK_Member_Nationality (Member_ID, Nationality_ID)
                    VALUES (%s, %s)
                    '''

                    cursor.execute(member_nation_link_sql, (member_id, nationality_id))
                
                for role_name in member_data.get('role', []):
                    
                
                    role_lookup_sql = "SELECT Role_ID FROM REF_Role WHERE Role_Name = %s"
                    cursor.execute(role_lookup_sql, (role_name,))
                    
                
                    result = cursor.fetchone()
                    
                    if result:
                        role_id = result[0]
                    else:
                   
                        raise ValueError(f"Selected role '{role_name}' not found in REF_Role database.")
                
                        
                    member_role_link_sql = '''
                    INSERT INTO LINK_Member_Role (Member_ID, Role_ID)
                    VALUES (%s, %s)
                    '''
                    # Now 'role_id' is the correct integer
                    cursor.execute(member_role_link_sql, (member_id, role_id))

            conn.commit()
            flash(f"Artist '{artist_data['artist_name']}' and {len(final_members_list)} members added successfully!", 'success')
            return redirect(url_for('main_routes.manage_artists')) 

        except mysql.connector.Error as err:
            conn.rollback()
            print(f"Database error: {err}")
            flash(f"An error occurred while creating the artist: {err.msg}", 'danger')
            return redirect(url_for('main_routes.add_artist')) 

        finally:
            if 'conn' in locals() and conn:
                conn.close()

    return add_artist_info()

def timedelta_to_time(td):
    """Converts a timedelta object to a time object (used for time fields)."""
    return (datetime.datetime.min + td).time()

@main_routes.route('/manage_artist/edit_artist/<int:artist_id>', methods=["GET", "POST"])
def edit_artist(artist_id):
    # --- 1. Fetch Reference Data (Roles and Nationalities) ---
    # Fetch all reference values for dropdowns
    role_query = "SELECT Role_ID, Role_Name FROM REF_Role ORDER BY Role_Name"
    nationality_query = "SELECT Nationality_ID, Nationality_Name FROM REF_Nationality ORDER BY Nationality_Name"

    dbroles = execute_select_query(role_query)
    dbnationalities = execute_select_query(nationality_query)

    roles = [{'id': row['Role_ID'], 'value': str(row['Role_Name']), 'text': str(row['Role_Name'])} for row in dbroles]
    nationalities = [{'id': row['Nationality_ID'], 'value': str(row['Nationality_Name']), 'text': str(row['Nationality_Name'])} for row in dbnationalities]

    # --- 2. GET Request: Fetch Existing Data ---
    if request.method == "GET":
        
        # A. Fetch Artist Core Data (Already robust and correct)
        artist_query = '''
        SELECT Artist_ID, Artist_Name, Debut_Date, Activity_Status
        FROM Artist
        WHERE Artist_ID = %s
        '''
        
        db_result = execute_select_query(artist_query, (artist_id,))
        
        if not db_result or not isinstance(db_result, list) or len(db_result) == 0:
            flash("Artist not found or database error.", 'error')
            return redirect(url_for('main_routes.artist_list'))
            
        artist_data = db_result[0]

        if artist_data.get('Debut_Date') and hasattr(artist_data['Debut_Date'], 'strftime'):
            artist_data['Debut_Date'] = artist_data['Debut_Date'].strftime('%Y-%m-%d')
        else:
            artist_data['Debut_Date'] = ''
        
        # B. Fetch Manager Data
        manager_query = '''
        SELECT Manager_ID, Agency, Manager_Name, Contact_Num, Contact_Email
        FROM Manager
        WHERE Artist_ID = %s
        '''
        manager_data_list = execute_select_query(manager_query, (artist_id,))
        manager_data = manager_data_list[0] if manager_data_list else {} # Ensure manager is a dict or empty dict
        
        # C. Fetch Member Data (Already robust and correct)
        members_query = '''
        SELECT 
            M.Member_ID, 
            M.Member_Name, 
            M.Birth_Date, 
            M.Activity_Status
        FROM Member M
        WHERE M.Artist_ID = %s
        '''
        dbmembers = execute_select_query(members_query, (artist_id,))
        
        initial_members = []
        for member in dbmembers:
            member_id = member['Member_ID']
            
            # Fetch Roles linked to this member
            member_roles_query = '''
            SELECT R.Role_Name 
            FROM REF_Role R JOIN LINK_Member_Role L ON R.Role_ID = L.Role_ID
            WHERE L.Member_ID = %s
            '''
            # Fetch Nationalities linked to this member
            member_nationalities_query = '''
            SELECT N.Nationality_Name 
            FROM REF_Nationality N JOIN LINK_Member_Nationality MN ON N.Nationality_ID = MN.Nationality_ID
            WHERE MN.Member_ID = %s
            '''
            
            roles_result = execute_select_query(member_roles_query, (member_id,))
            nationalities_result = execute_select_query(member_nationalities_query, (member_id,))
            
            member_roles = [r['Role_Name'] for r in roles_result]
            member_nationalities = [n['Nationality_Name'] for n in nationalities_result]
            
            birth_date_str = member.get('Birth_Date')
            if birth_date_str and hasattr(birth_date_str, 'strftime'):
                 birth_date_str = birth_date_str.strftime('%Y-%m-%d')
            else:
                 birth_date_str = ''

            initial_members.append({
                'member_id': member['Member_ID'],
                'name': member['Member_Name'],
                'birth_date': birth_date_str,
                'activity_status': member['Activity_Status'],
                'roles': member_roles,
                'nationalities': member_nationalities
            })

        return render_template(
            'edit_artist.html',
            artist=artist_data,
            manager=manager_data,
            initial_members=initial_members,
            roles=roles,
            nationalities=nationalities
        )

    # --- 3. POST Request: Handle Update ---
    elif request.method == "POST":
        try:
            form = request.form
            
            # 1. Extract Artist Data (No changes needed)
            artist_name = form.get('artist_name')
            debut_date_str = form.get('debut_date')
            activity_status = form.get('activity_status')
            
            if not all([artist_name, debut_date_str, activity_status]):
                flash("Missing required Artist Name, Debut Date, or Activity Status.", 'error')
                return redirect(request.url)
            
            debut_date = datetime.datetime.strptime(debut_date_str, '%Y-%m-%d').date()

    
            update_artist_query = '''
            UPDATE Artist 
            SET Artist_Name = %s, Debut_Date = %s, Activity_Status = %s
            WHERE Artist_ID = %s
            '''
            update_artist_params = (artist_name, debut_date, activity_status, artist_id)
            execute_modified_insert(update_artist_query, update_artist_params)

        
            manager_id = form.get('manager_id')
            agency = form.get('agency')
            manager_name = form.get('manager_name')
            contact_num = form.get('contact_num')
            contact_email = form.get('contact_email') 

            if manager_id:
            
                manager_query = '''
                UPDATE Manager 
                SET Agency = %s, Manager_Name = %s, Contact_Num = %s, Contact_Email = %s
                WHERE Manager_ID = %s
                ''' 
                manager_params = (agency, manager_name, contact_num, contact_email, manager_id) 
            elif any([agency, manager_name, contact_num, contact_email]):
               
                manager_query = '''
                INSERT INTO Manager (Artist_ID, Agency, Manager_Name, Contact_Num, Contact_Email)
                VALUES (%s, %s, %s, %s, %s)
                '''
                manager_params = (artist_id, agency, manager_name, contact_num, contact_email)
            else:
                manager_query = None 

            if manager_query:
                execute_modified_insert(manager_query, manager_params)
         
            existing_member_ids_query = "SELECT Member_ID FROM Member WHERE Artist_ID = %s"
            existing_member_ids = {m['Member_ID'] for m in execute_select_query(existing_member_ids_query, (artist_id,))}
            
         
            members_map = {}
            for key in form:
                if key.startswith('members['):
                   
                    import re
                    match = re.search(r'members\[(\d+)\]\[(.*?)\]', key)
                    if match:
                        index = int(match.group(1))
                        field = match.group(2)
                        
                        if index not in members_map:
                            members_map[index] = {'member_id': None, 'name': None, 'birth_date': None, 'activity_status': 'Active', 'role': [], 'nationality': []}
                        
               
                        if field in ('role', 'nationality'):
                           
                            members_map[index][field] = form.getlist(key) 
                        else:
                            # Standard singular fields
                            members_map[index][field] = form.get(key)

            # Convert the map to a list, sorted by index
            final_members_list = [v for k, v in sorted(members_map.items())]
    
            
            form_member_ids = set()

            for member_data in final_members_list:
                member_id = member_data.get('member_id')
                member_name = member_data.get('name')
                birth_date_str = member_data.get('birth_date')
                activity_status = member_data.get('activity_status')
                
                # Roles and Nationalities are now directly in member_data as lists (from the fix)
                member_roles = member_data.get('role', [])
                member_nationalities = member_data.get('nationality', [])
                
                if not member_name or not activity_status or not birth_date_str:
                    # Skip members that were partially filled or blank new rows
                    continue 
                
                # Standardize data types
                birth_date = datetime.datetime.strptime(birth_date_str, '%Y-%m-%d').date()

                # Get ID mapping for references
                role_ids = [r['id'] for r in roles if r['value'] in member_roles]
                nationality_ids = [n['id'] for n in nationalities if n['value'] in member_nationalities]

                if member_id and str(member_id).isdigit() and int(member_id) in existing_member_ids:
                    # UPDATE EXISTING MEMBER
                    member_id = int(member_id)
                    form_member_ids.add(member_id)
                    
                    update_member_query = '''
                    UPDATE Member 
                    SET Member_Name = %s, Birth_Date = %s, Activity_Status = %s
                    WHERE Member_ID = %s
                    '''
                    execute_modified_insert(update_member_query, (member_name, birth_date, activity_status, member_id))
                    
                else:
                    # INSERT NEW MEMBER
                    insert_member_query = '''
                    INSERT INTO Member (Artist_ID, Member_Name, Birth_Date, Activity_Status)
                    VALUES (%s, %s, %s, %s)
                    '''
           
                    member_id = execute_modified_insert(insert_member_query, (artist_id, member_name, birth_date, activity_status), return_id=True)
                    form_member_ids.add(member_id)
                
                # Delete old links
                execute_modified_insert("DELETE FROM LINK_Member_Role WHERE Member_ID = %s", (member_id,))
                execute_modified_insert("DELETE FROM LINK_Member_Nationality WHERE Member_ID = %s", (member_id,))

                # Insert new Role links
                if role_ids:
                    link_role_query = "INSERT INTO LINK_Member_Role (Member_ID, Role_ID) VALUES (%s, %s)"
                    for role_id in role_ids:
                        execute_modified_insert(link_role_query, (member_id, role_id))

                # Insert new Nationality links
                if nationality_ids:
                    link_nationality_query = "INSERT INTO LINK_Member_Nationality (Member_ID, Nationality_ID) VALUES (%s, %s)"
                    for nationality_id in nationality_ids:
                        execute_modified_insert(link_nationality_query, (member_id, nationality_id))

            members_to_delete = existing_member_ids - form_member_ids
                        
            if members_to_delete:
                member_id_list = list(members_to_delete)
                
                # Dynamically generate the IN clause placeholders: (%s, %s, %s, ...)
                placeholders = ', '.join(['%s'] * len(member_id_list))
                
                # Delete links (Roles)
                delete_role_query = f"DELETE FROM LINK_Member_Role WHERE Member_ID IN ({placeholders})"
                execute_modified_insert(delete_role_query, member_id_list)
                
                # Delete links (Nationalities)
                delete_nat_query = f"DELETE FROM LINK_Member_Nationality WHERE Member_ID IN ({placeholders})"
                execute_modified_insert(delete_nat_query, member_id_list)

                # Then delete the members
                delete_member_query = f"DELETE FROM Member WHERE Member_ID IN ({placeholders})"
                execute_modified_insert(delete_member_query, member_id_list)

                
            flash("Artist details updated successfully!", 'success')
            return redirect(url_for('main_routes.manage_artists'))

        except Exception as e:
            flash(f"An unexpected error occurred during update: {e}", 'error')
            return redirect(request.url)




@main_routes.route('/manage_events')
def manage_events():
    event_query = '''
    SELECT e.*, v.Venue_Name
    FROM Event e
    JOIN Venue v ON e.Venue_ID = v.Venue_ID
    ORDER BY e.Event_ID 
    '''
    
    events = execute_select_query(event_query)

    return render_template(
        'manage_events.html',
        events=events
    )

@main_routes.route('/manage_events/add_event', methods=["GET","POST"])
def add_event():
    if request.method == 'POST':
        print("Hello")

    type_query = '''
    SELECT et.Type_ID, et.Type_Name, et.Artist_Event_Only
    FROM REF_Event_Type et
    '''
    artist_query = '''
    SELECT Artist_ID, Artist_Name
    FROM Artist
    ORDER BY Artist_Name 
    '''
    fanclub_query = '''
    SELECT Fanclub_ID, Fanclub_Name
    FROM Fanclub
    ORDER BY Fanclub_Name 
    '''
    venue_query = '''
    SELECT Venue_ID, Venue_Name
    FROM Venue
    ORDER BY Venue_Name 
    '''
    
    event_types = execute_select_query(type_query)
    artists = execute_select_query(artist_query)
    fanclubs = execute_select_query(fanclub_query)
    venues = execute_select_query(venue_query)

    if request.method == 'POST':
        try:
            form = request.form
            # Event Record
            event_name = form.get('event_name')
            event_category = form.get('event-category')
            event_types_list = form.getlist('event-type') # <-- Changed to getlist

            venue_id = form.get('venue_id', type=int)
            start_date_str = form.get('start_date')
            end_date_str = form.get('end_date')
            start_time_str = form.get('start_time')
            end_time_str = form.get('end_time')
            
            if not all([event_name, event_types_list, venue_id, start_date_str, start_time_str, end_time_str]):
                flash("Missing required event information.", 'error')
                return redirect(request.url)
            
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            start_time = datetime.datetime.strptime(start_time_str, '%H:%M').time()
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else start_date
            end_time = datetime.datetime.strptime(end_time_str, '%H:%M').time()

            new_event = '''
            INSERT INTO Event (Event_Name, Venue_ID, Start_Date, End_Date, Start_Time, End_Time)
            VALUES (%s, %s, %s, %s, %s, %s)
            '''
            new_event_params = (
                event_name, venue_id, start_date, end_date, start_time, end_time, 
            )

            overlap_query = """
            SELECT e.Event_ID, e.Event_Name
            FROM Event e
            WHERE 
                e.Venue_ID = %s 
                AND e.Event_ID != %s 
                AND e.End_Date >= %s AND e.Start_Date <= %s
                AND ( (e.Start_Date = %s AND e.End_Date = %s AND %s < e.End_Time AND %s > e.Start_Time) OR e.Start_Date < %s OR %s < e.End_Date )
            LIMIT 1;
            """
            
            overlap_params = (
                venue_id, 0, # Pass 0 or NULL to ignore the exclusion check
                end_date, start_date, 
                start_date, end_date, 
                start_time, end_time,
                start_date, end_date
            )

            overlap_result = execute_select_query(overlap_query, overlap_params)
            
            if overlap_result:
                overlapping_event = overlap_result[0]
                flash(f"Date Conflict: Event '{overlapping_event['Event_Name']}' (ID: {overlapping_event['Event_ID']}) is already scheduled at this venue during the requested time.", 'error')
                return redirect(request.url)

            # Commit into database
            event_id = execute_modified_insert(new_event, new_event_params)
            print("EVENT_ID RECEIVED", event_id)
            
            if not event_id:
                flash("Failed to create event record.", 'error')
                return redirect(url_for('main_routes.add_event'))

            # Determine event category:  [CHANGE TO LIST LATER]
            artist_id = form.get('artist', type=int) if event_category == 'artist-event' else None
            fanclub_id = form.get('fanclub', type=int) if event_category == 'fanclub-event' else None

            # Artist_Event or Fanclub_Event
            if event_category == 'artist-event' and not artist_id:
                # Additional validation needed if no artist is selected
                flash('Please select an artist for the event.', 'error')
                return redirect(url_for('main_routes.add_event'))
            elif event_category == 'fanclub-event' and not fanclub_id:
                # Additional validation needed if no fanclub is selected
                flash('Please select a fanclub for the event.', 'error')
                return redirect(url_for('main_routes.add_event'))
    
            tier_ids = form.getlist('tier_id[]')
            tier_names = form.getlist('tier_name[]')
            tier_prices = form.getlist('tier_price[]')
            tier_quantities = form.getlist('tier_quantity[]')
            tier_benefits = form.getlist('tier_benefits[]')

            ticket_tiers_data = []

            type_junction_sql = "INSERT INTO LINK_Event_Type (Event_ID, Type_ID) VALUES (%s, %s)"
            for type_id_str in event_types_list:
                execute_insert_query(type_junction_sql, (event_id, int(type_id_str)))
            
            for tier_id, name, price_str, quantity_str, benefits in zip(
                tier_ids, tier_names, tier_prices, tier_quantities, tier_benefits
            ):
                sections = form.getlist(f'tier_sections_{tier_id}[]')
                is_reserved_seating = int(form.get(f'tier_reserved_seating_{tier_id}'))

                try:
                # Convert strings to their appropriate types
                    price = float(price_str)
                    quantity = int(quantity_str)
                except ValueError:
                    flash(f"Invalid price or quantity for tier ID {tier_id}.", 'error')
                    return redirect(url_for('main_routes.create_event_page'))
            
                tier_data = {
                    'id': int(tier_id),
                    'name': name,
                    'price': price,
                    'quantity': quantity,
                    'benefits': benefits if benefits != "" else None,
                    'sections': [int(s) for s in sections], # Convert section IDs to integers
                    'is_reserved_seating': is_reserved_seating
                }
                ticket_tiers_data.append(tier_data)

            # Ticket Tier Records
            # Insert into Artist/Fanclub Junction Table
            if event_category == 'artist-event':
                execute_insert_query(
                    "INSERT INTO Artist_Event (Artist_ID, Event_ID) VALUES(%s, %s)", 
                    (artist_id, event_id)
                )
            elif event_category == 'fanclub-event':
                execute_insert_query(
                    "INSERT INTO Fanclub_Event (Fanclub_ID, Event_ID) VALUES(%s, %s)", 
                    (fanclub_id, event_id) 
                )
            
            # Insert into 
            new_tier = '''
            INSERT INTO Ticket_Tier(Event_ID, Tier_Name, Price, Total_Quantity, Benefits, Is_Reserved_Seating)
            VALUES (%s, %s, %s, %s, %s, %s)
            '''
            new_tier_section = '''
            INSERT INTO Tier_Section(Tier_ID, Section_ID) VALUES (%s, %s)
            '''

            if not ticket_tiers_data:
                execute_insert_query(new_tier, (event_id, "Event Entry", 0.0, None, None, 0))

            for tier in ticket_tiers_data:
                tier_params = (
                    event_id, tier['name'], tier['price'], tier['quantity'],
                    tier['benefits'], tier['is_reserved_seating']
                )

                tier_id = execute_modified_insert(new_tier, tier_params)

                if not tier_id:
                    flash(f"Failed to create ticket tier: {tier['name']}.", 'warning')
                    continue

                for section_id in tier['sections']:
                    execute_insert_query(new_tier_section, (tier_id, section_id))

            
            flash('Event and all associated data created successfully!', 'success')
            return redirect(url_for('main_routes.manage_events', event_id=event_id))

        except Exception as e:
            flash(f"An unexpected error occurred. {e}", 'error')

    return render_template(
        'add_event.html',
        event_types=event_types,
        artists=artists,
        fanclubs=fanclubs,
        venues=venues
    )

@main_routes.route('/api/venue/<int:venue_id>/sections', methods=['GET'])
def get_venue_sections(venue_id):  
    
    sections_query = '''
        SELECT Section_ID, Section_Name, Max_Capacity AS Capacity, Venue_ID
        FROM Section
        WHERE Venue_ID = %s
        ORDER BY Section_Name
    '''

    sections_data = execute_select_query(sections_query, (venue_id,))

    return jsonify({'sections': sections_data})

def timedelta_to_time(td):
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return datetime.time(hour=hours, minute=minutes, second=seconds)

@main_routes.route('/manage_events/edit_event/<int:event_id>', methods=["GET","POST"])
def edit_event(event_id):  
    event_detail_query = '''
    SELECT 
        e.Event_ID, e.Event_Name, e.Start_Date, e.End_Date, e.Start_Time, e.End_Time,
        ae.Artist_ID, fe.Fanclub_ID, v.Venue_Name, v.Venue_ID
    FROM Event e
    JOIN Venue v ON e.Venue_ID = v.Venue_ID
    LEFT JOIN Artist_Event ae ON e.Event_ID = ae.Event_ID
    LEFT JOIN Fanclub_Event fe ON e.Event_ID = fe.Event_ID
    WHERE e.Event_ID = %s
    '''

    event_types_query = "SELECT * FROM REF_Event_Type"
    event_type_ids_query = "SELECT Event_ID, Type_ID FROM LINK_Event_Type WHERE Event_ID = %s"
    event_types = execute_select_query(event_types_query)
    event_type_ids = execute_select_query(event_type_ids_query, (event_id,))

    event_data_sql = execute_select_query(event_detail_query, (event_id,))
    event_data = event_data_sql[0]
    if not event_data:
        flash("Event not found.", 'error')
        return redirect(url_for('main_routes.manage_events')) # Assuming this is the event list page

    if event_data["Start_Date"]:
        event_data["Start_Date"] = event_data["Start_Date"].strftime("%Y-%m-%d")

    if event_data["End_Date"]:
        event_data["End_Date"] = event_data["End_Date"].strftime("%Y-%m-%d")

    if event_data["Start_Time"]:
        if isinstance(event_data["Start_Time"], datetime.timedelta):
            t = timedelta_to_time(event_data["Start_Time"])
            event_data["Start_Time"] = t.strftime("%H:%M")  # for HTML <input type="time">
        elif isinstance(event_data["Start_Time"], str):
            t = datetime.datetime.strptime(event_data["Start_Time"], "%H:%M:%S").time()
            event_data["Start_Time"] = t.strftime("%H:%M")

    if event_data["End_Time"]:
        if isinstance(event_data["End_Time"], datetime.timedelta):
            t = timedelta_to_time(event_data["End_Time"])
            event_data["End_Time"] = t.strftime("%H:%M")
        elif isinstance(event_data["End_Time"], str):
            t = datetime.datetime.strptime(event_data["End_Time"], "%H:%M:%S").time()
            event_data["End_Time"] = t.strftime("%H:%M")
    
    if request.method == 'POST':
        try:
            form = request.form
            
            # Event Record
            event_name = form.get('event_name')
            event_types_list = form.getlist('event-type') 
            start_date_str = form.get('start_date')
            end_date_str = form.get('end_date')      # Optional
            start_time_str = form.get('start_time')
            end_time_str = form.get('end_time')
            venue_id = form.get('venue_')
            
            print("CHECK", event_name, start_date_str, start_time_str, end_time_str)
            if not all([event_name, start_date_str, start_time_str, end_time_str]) or not event_types_list:
                flash("Missing required event information. Please check Event Name, all Date/Time fields, and select at least one Event Type.", 'error')
                return redirect(request.url)
                
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            start_time = datetime.datetime.strptime(start_time_str, '%H:%M').time()
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else start_date
            end_time = datetime.datetime.strptime(end_time_str, '%H:%M').time()

            overlap_query = """
            SELECT e.Event_ID, e.Event_Name
            FROM Event e
            WHERE 
                e.Venue_ID = %s 
                AND e.Event_ID != %s 
                AND e.End_Date >= %s AND e.Start_Date <= %s
                AND ( (e.Start_Date = %s AND e.End_Date = %s AND %s < e.End_Time AND %s > e.Start_Time) OR e.Start_Date < %s OR %s < e.End_Date )
            LIMIT 1;
            """
            
            overlap_params = (
                venue_id, 0, # Pass 0 or NULL to ignore the exclusion check
                end_date, start_date, 
                start_date, end_date, 
                start_time, end_time,
                start_date, end_date
            )

            overlap_result = execute_select_query(overlap_query, overlap_params)
            
            if overlap_result:
                overlapping_event = overlap_result[0]
                flash(f"Date Conflict: Event '{overlapping_event['Event_Name']}' (ID: {overlapping_event['Event_ID']}) is already scheduled at this venue during the requested time.", 'error')
                return redirect(request.url)

            update_event_query = '''
            UPDATE Event 
            SET Event_Name = %s, Start_Date = %s, End_Date = %s, Start_Time = %s, End_Time = %s
            WHERE Event_ID = %s
            '''
            update_event_params = (
                event_name, start_date, end_date, start_time, end_time, event_id
            )

            rows_affected = execute_modified_insert(update_event_query, update_event_params)
            print("EVENT_ID RECEIVED", event_id)
            
            if rows_affected is None:
                flash("Failed to update event record.", 'error')
                return redirect(url_for('main_routes.manage_events'))
            

            # For event types
            delete_links_query = "DELETE FROM LINK_Event_Type WHERE Event_ID = %s"
            execute_modified_insert(delete_links_query, (event_id,)) 
            event_types_list = form.getlist('event-type') # List of Type_IDs from the form

            if event_types_list:
                insert_links_query = "INSERT INTO LINK_Event_Type (Event_ID, Type_ID) VALUES (%s, %s)"
                
                # Loop through the list of Type IDs received from the form
                for type_id in event_types_list:
                    link_params = (event_id, type_id)
                    execute_modified_insert(insert_links_query, link_params) 
                    
            flash("Event updated successfully!", 'success')
            return redirect(url_for('main_routes.manage_events'))
                    
        except Exception as e:
            flash(f"An unexpected error occurred. {e}", 'error')

    return render_template(
        'edit_event.html',
        event_id=event_id,
        event_data=event_data,
        event_types=event_types,
        event_type_ids=event_type_ids
    )

@main_routes.route('/delete_event/<int:event_id>', methods=["GET"])
def delete_event(event_id):
    try:
        check_purchases_query = """
        SELECT COUNT(*) AS total_purchases
        FROM Ticket_Purchase tp
        JOIN Ticket_Tier tt ON tp.Tier_ID = tt.Tier_ID
        WHERE tt.Event_ID = %s
        """
        
        purchase_data = execute_select_query(check_purchases_query, (event_id,))
        
        total_purchases = purchase_data[0]['total_purchases'] if purchase_data else 0

        if total_purchases > 0:
            flash(f"Deletion Failed: Event ID {event_id} has {total_purchases} existing ticket purchase(s). You must cancel or refund tickets before deleting.", 'error')
            return redirect(url_for('main_routes.manage_events'))

        
        # Delete from all linking/child tables:
        execute_insert_query("DELETE FROM LINK_Event_Type WHERE Event_ID = %s", (event_id,))
        execute_insert_query("DELETE FROM Artist_Event WHERE Event_ID = %s", (event_id,))
        execute_insert_query("DELETE FROM Fanclub_Event WHERE Event_ID = %s", (event_id,))
        execute_insert_query("DELETE FROM Ticket_Tier WHERE Event_ID = %s", (event_id,))
        
        delete_event_query = "DELETE FROM Event WHERE Event_ID = %s"
        execute_insert_query(delete_event_query, (event_id,))
        
        flash(f"Event ID {event_id} and all related data deleted successfully.", 'success')
        
    except Exception as e:
        flash(f"An unexpected error occurred while deleting event {event_id}: {e}", 'error')
    
    return redirect(url_for('main_routes.manage_events'))

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
        event_id=event_id,
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

@main_routes.route('/setlist/view/<int:event_id>')
def view_setlist(event_id):
    event_query = """
    SELECT e.Event_Name, DATE_FORMAT(e.Start_Date, '%Y-%m-%d') AS event_date, v.Venue_Name
    FROM Event e
    JOIN Venue v ON e.Venue_ID = v.Venue_ID
    WHERE e.Event_ID = %s
    """
    event_data = execute_select_query(event_query, (event_id,))
    if not event_data:
        return redirect(url_for('main_routes.events'))


    event = event_data[0]

    artist_query = """
    SELECT a.Artist_ID, a.Artist_Name
    FROM Artist a
    JOIN Artist_Event ae ON a.Artist_ID = ae.Artist_ID
    WHERE ae.Event_ID = %s
    """
    artists = execute_select_query(artist_query, (event_id,))

    setlist_query = """
    SELECT sl.Song_ID, sl.Play_Order, s.Song_Name
    FROM Setlist sl
    JOIN Song s ON sl.Song_ID = s.Song_ID
    WHERE sl.Event_ID = %s
    ORDER BY sl.Play_Order ASC
    """
    setlist_records = execute_select_query(setlist_query, (event_id,))
    
    all_songs_query = '''
    SELECT 
        s.Song_ID, 
        s.Song_Name 
    FROM 
        Song s
    JOIN 
        Setlist sl ON s.Song_ID = sl.Song_ID 
    WHERE 
        sl.Event_ID = %s  -- Filter by the specific event ID
    ORDER BY 
        s.Song_Name ASC
        '''
    all_songs = execute_select_query(all_songs_query, (event_id,))

    return render_template(
        'setlist_view.html',
        event_id=event_id,
        event_name=event['Event_Name'],
        event_date=event['event_date'],
        venue_name=event['Venue_Name'],
        artists=artists,
        setlist_records=setlist_records,
        all_songs=all_songs
    )

# ============================================
#           Fanclub Subpages
# ============================================

@main_routes.route('/fanclubs/<int:fanclub_id>')
def fanclub_details(fanclub_id):

    current_fan_id = g.current_user['Fan_ID'] if g.current_user else None

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

    current_fan_id = g.current_user['Fan_ID'] if g.current_user else None

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

    current_fan_id = g.current_user['Fan_ID'] if g.current_user else None

    insert_fanclub_membership_record = '''
    INSERT INTO Fanclub_Membership (Fan_ID, Fanclub_ID)
    VALUES (%s, %s)
    '''

    execute_insert_query(insert_fanclub_membership_record, (current_fan_id, fanclub_id))
    
    flash(f"You successfully joined this fanclub!", "success")
    return redirect(url_for('main_routes.fanclub_details', fanclub_id=fanclub_id))

@main_routes.route('/fanclubs/<int:fanclub_id>/leave', methods=['POST'])
def leave_fanclub(fanclub_id):

    current_fan_id = g.current_user['Fan_ID'] if g.current_user else None

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
        FROM LINK_Member_Role AS mr
        JOIN REF_Role AS r ON mr.Role_ID = r.Role_ID
        JOIN Member AS me ON mr.Member_ID = me.Member_ID
        WHERE me.Artist_ID = %s
        '''
    
    member_nationality_query = '''
        SELECT mn.Member_ID, 
            n.Nationality_Name 
        FROM LINK_Member_Nationality AS mn
        JOIN REF_Nationality AS n ON mn.Nationality_ID = n.Nationality_ID
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
    
    current_fan_id = g.current_user['Fan_ID'] if g.current_user else None
    
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

    current_fan_id = g.current_user['Fan_ID'] if g.current_user else None
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
                db_conn.rollback() 
                flash(f"⚠️ Stock Error: '{merch_name}' is sold out. Please update your cart.", 'danger')
                cursor.close()
                return redirect(url_for('main_routes.cart'))

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
            
@main_routes.route('/manage_merchandise')
def manage_merchandise():
    query = '''
    SELECT 
        M.*, 
        A.Artist_Name,
        F.Fanclub_Name,
        GROUP_CONCAT(DISTINCT E.Event_ID SEPARATOR ', ') AS Event_IDs,
        GROUP_CONCAT(DISTINCT E.Event_Name SEPARATOR ', ') AS Event_Names
    FROM 
        Merchandise AS M
    LEFT JOIN 
        Artist AS A ON M.Artist_ID = A.Artist_ID
    LEFT JOIN 
        Fanclub AS F ON M.Fanclub_ID = F.Fanclub_ID
    LEFT JOIN Merchandise_Event ME ON M.Merchandise_ID = ME.Merchandise_ID
    LEFT JOIN Event E ON ME.Event_ID = E.Event_ID
    GROUP BY
        M.Merchandise_ID, A.Artist_Name, F.Fanclub_Name 
    ORDER BY
        M.Merchandise_ID
    '''

    # The result will contain an 'Event_Names' column with a comma-separated list
    merchandise = execute_select_query(query)

    return render_template(
        'manage_merchandise.html', 
        merchandise=merchandise
    )
            
@main_routes.route('/add_merchandise', methods=['GET', 'POST'])
def add_merchandise():
    if request.method == 'GET':
        try:
            events = execute_select_query("SELECT Event_ID, Event_Name FROM Event ORDER BY Event_Name")
            artists = execute_select_query("SELECT Artist_ID, Artist_Name FROM Artist ORDER BY Artist_Name")
            fanclubs = execute_select_query("SELECT Fanclub_ID, Fanclub_Name FROM Fanclub ORDER BY Fanclub_Name")
        except Exception as e:
            print(f"Error fetching form data: {e}")
            flash('Could not load form options due to a database error.', 'error')
            events, artists, fanclubs = [], [], []

        return render_template('add_merchandise.html', 
            events=events, 
            artists=artists, 
            fanclubs=fanclubs
        )

    elif request.method == 'POST':
        merch_name = request.form.get('merchandise_name')
        merch_desc = request.form.get('merchandise_description')
        merch_price = request.form.get('merchandise_price')
        initial_stock = request.form.get('initial_stock')
        
        artist_id = request.form.get('artist_id') if request.form.get('artist_id') else None
        fanclub_id = request.form.get('fanclub_id') if request.form.get('fanclub_id') else None
        
        selected_event_ids = request.form.getlist('event_ids')
        
        
        if not all([merch_name, merch_price, initial_stock]):
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('main_routes.add_merchandise'))

        if not (artist_id or fanclub_id or selected_event_ids):
            flash('Merchandise must be associated with at least one Event, Artist, or Fanclub.', 'error')
            return redirect(url_for('main_routes.add_merchandise'))
        
        new_merchandise_id = None
        
        try:
            price = float(merch_price)
            stock = int(initial_stock)
            
            merchandise_insert_query = """
                INSERT INTO Merchandise (Merchandise_Name, Merchandise_Description, Merchandise_Price, Initial_Stock, Quantity_Stock, Artist_ID, Fanclub_ID)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            merchandise_params = (merch_name, merch_desc, price, stock, stock, artist_id, fanclub_id)
            
            new_merchandise_id = execute_select_one_query(merchandise_insert_query, merchandise_params)
            
            if not new_merchandise_id:
                raise Exception("Failed to retrieve the new Merchandise ID after insertion. Check execute_insert_query.")

            if selected_event_ids:
                insert_junction_query = "INSERT INTO Merchandise_Event (Merchandise_ID, Event_ID) VALUES (%s, %s)"
                
                for event_id_str in selected_event_ids:
                    event_id = int(event_id_str) 
                    junction_params = (new_merchandise_id, event_id)
                    execute_select_one_query(insert_junction_query, junction_params)
            
            
            flash(f'Merchandise "{merch_name}" successfully created and linked!', 'success')
            return redirect(url_for('main_routes.manage_merchandise'))

        except ValueError:
            flash('Invalid input for Price or Stock quantities. Please enter valid numbers.', 'error')
            return redirect(url_for('main_routes.add_merchandise'))
            
        except Exception as e:
            flash(f'An internal error occurred during creation: {e}', 'error')
            return redirect(url_for('main_routes.add_merchandise'))
        

@main_routes.route('/manage_merchandise/<int:merchandise_id>/edit_merchandise', methods=['GET', 'POST'])
def edit_merchandise(merchandise_id):
    artist_query = "SELECT Artist_ID, Artist_Name FROM Artist ORDER BY Artist_Name"
    artists = execute_select_query(artist_query)
    
    events_query = "SELECT Event_ID, Event_Name FROM Event ORDER BY Event_Name"
    events = execute_select_query(events_query)
    
    fanclub_query = "SELECT Fanclub_ID, Fanclub_Name FROM Fanclub ORDER BY Fanclub_Name"
    fanclubs = execute_select_query(fanclub_query)

    merchandise_query = '''
    SELECT 
        Merchandise_ID, Merchandise_Name, Merchandise_Description, Merchandise_Price, 
        Initial_Stock, Quantity_Stock, Artist_ID, Fanclub_ID
    FROM Merchandise 
    WHERE Merchandise_ID = %s
    '''
    merchandise_data = execute_select_query(merchandise_query, (merchandise_id,))
    
    if not merchandise_data:
        flash("Merchandise not found.", 'error')
        return redirect(url_for('main_routes.manage_merchandise'))
        
    merchandise = merchandise_data[0]

    associated_events_query = '''
        SELECT Event_ID
        FROM Merchandise_Event
        WHERE Merchandise_ID = %s
    '''

    associated_event_ids = [row['Event_ID'] for row in execute_select_query(associated_events_query, (merchandise_id,))]

    
    if request.method == 'POST':
        selected_event_ids_int = []
        
        try:
            new_name = request.form.get('merchandise_name')
            new_description = request.form.get('merchandise_description', '') 
            
            new_price = float(request.form.get('merchandise_price'))
            new_initial_stock = int(request.form.get('initial_stock'))
            new_quantity_stock = int(request.form.get('quantity_stock'))
            
            selected_event_ids_str = request.form.getlist('event_ids')
            selected_event_ids_int = [int(eid) for eid in selected_event_ids_str if eid.isdigit()]

            new_artist_id = request.form.get('artist_id')
            new_fanclub_id = request.form.get('fanclub_id')
            
            def render_error_state(msg, event_ids_to_check):
                flash(msg, 'error')
                merchandise.update({
                    'Merchandise_Name': new_name, 'Merchandise_Description': new_description, 
                    'Merchandise_Price': new_price, 'Initial_Stock': new_initial_stock, 
                    'Quantity_Stock': new_quantity_stock, 'Artist_ID': new_artist_id, 
                    'Fanclub_ID': new_fanclub_id,
                })
                return render_template(
                    'edit_merchandise.html', 
                    merchandise=merchandise, 
                    artists=artists, 
                    events=events, 
                    fanclubs=fanclubs, 
                    associated_event_ids=event_ids_to_check 
                )

            # --- Validation Checks ---
            if not all([new_name, new_price is not None, new_initial_stock is not None, new_quantity_stock is not None]):
                return render_error_state("All basic fields (Name, Price, and Stock Quantities) are required.", selected_event_ids_int)
                
            if new_quantity_stock > new_initial_stock:
                return render_error_state("Quantity in Stock cannot be greater than Initial Stock Quantity.", selected_event_ids_int)
                
            is_artist_set = bool(new_artist_id and new_artist_id.strip())
            is_fanclub_set = bool(new_fanclub_id and new_fanclub_id.strip())
            is_event_set = bool(selected_event_ids_int)

            if not (is_event_set or is_artist_set or is_fanclub_set):
                return render_error_state("Merchandise must be associated with at least one: an Event, an Artist, or a Fanclub.", selected_event_ids_int)

            # Check for name uniqueness
            if new_name != merchandise['Merchandise_Name']:
                check_name_query = "SELECT Merchandise_ID FROM Merchandise WHERE Merchandise_Name = %s AND Merchandise_ID != %s"
                existing_merch = execute_select_query(check_name_query, (new_name, merchandise_id))

                if existing_merch:
                    return render_error_state(f"A merchandise item named '{new_name}' already exists. Please choose a unique name.", selected_event_ids_int)


            artist_id_param = new_artist_id if is_artist_set else None
            fanclub_id_param = new_fanclub_id if is_fanclub_set else None
            
            update_merchandise_query = '''
            UPDATE Merchandise
            SET 
                Merchandise_Name = %s, Merchandise_Description = %s, Merchandise_Price = %s,
                Initial_Stock = %s, Quantity_Stock = %s, Artist_ID = %s, Fanclub_ID = %s
                WHERE Merchandise_ID = %s
            '''
            
            params = (
                new_name, new_description, new_price,
                new_initial_stock, new_quantity_stock,
                artist_id_param, fanclub_id_param,
                merchandise_id 
            )

            execute_insert_query(update_merchandise_query, params)


            delete_junction_query = "DELETE FROM Merchandise_Event WHERE Merchandise_ID = %s"
            execute_insert_query(delete_junction_query, (merchandise_id,)) 


            if selected_event_ids_int:
                insert_junction_query = "INSERT INTO Merchandise_Event (Merchandise_ID, Event_ID) VALUES (%s, %s)"
                
                for event_id in selected_event_ids_int:
                    junction_params = (merchandise_id, event_id)
                    execute_select_one_query(insert_junction_query, junction_params)
            
            
            flash(f"Merchandise '{new_name}' updated successfully!", 'success')
            return redirect(url_for('main_routes.manage_merchandise'))
        
        except ValueError:
        
            return render_error_state("Invalid input for Price or Stock quantities. Please enter valid numbers.", selected_event_ids_int)
            
        except Exception as e:
            return render_error_state(f"An unexpected error occurred while updating the merchandise: {e}", associated_event_ids) # Use original IDs here


    return render_template(
        'edit_merchandise.html', 
        merchandise=merchandise, 
        artists=artists, 
        events=events, 
        fanclubs=fanclubs,
        associated_event_ids=associated_event_ids 
    )

@main_routes.route('/manage_merchandise/<int:merchandise_id>/delete_merchandise', methods=['POST'])
def delete_merchandise(merchandise_id):
    merchandise_name_query = "SELECT Merchandise_Name FROM Merchandise WHERE Merchandise_ID = %s"
    merchandise_data = execute_select_query(merchandise_name_query, (merchandise_id,))
    
    if not merchandise_data:
        flash("Merchandise item not found.", 'error')
        return redirect(url_for('main_routes.manage_merchandise'))

    merchandise_name = merchandise_data[0]['Merchandise_Name']
    
    try:
        delete_query = '''
        DELETE FROM Merchandise
        WHERE Merchandise_ID = %s
        '''
        
        execute_insert_query(delete_query, (merchandise_id,))

        # SUCCESS
        flash(f"Merchandise '{merchandise_name}' successfully deleted.", 'success')
        return redirect(url_for('main_routes.manage_merchandise'))
        
    except Exception as e:
        flash(f"Error deleting merchandise '{merchandise_name}'. It is currently associated with active records (e.g., Orders). Please delete associated orders first. Error: {e}", 'error')
        return redirect(url_for('main_routes.manage_merchandise'))


@main_routes.route('/purchase_list')
def purchaseList():
    current_fan_id = session.get('fan_id')
    db_conn = None
    
    if not current_fan_id:
        purchase_display_data = []
        purchase_total = 0.0
        item_count = 0
    else:
        purchase_display_data = []
        purchase_total = 0.0
        total_units = 0
        
        try:
            db_conn = get_conn()
            cursor = db_conn.cursor(dictionary=True)
            
            sql_query = """
            SELECT
                PL.Purchase_List_ID AS pl_id,
                O.Order_ID AS order_id,
                M.Merchandise_Name AS name,
                COALESCE(A.Artist_Name, F.Fanclub_Name) AS artist,
                M.Merchandise_Price AS price,
                PL.Quantity_Purchased AS quantity,
                O.Order_Status AS status
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
                AND O.Order_Status = 'Paid';
            """
            
            cursor.execute(sql_query, (current_fan_id,))
            
            for item in cursor.fetchall():
                purchase_display_data.append(item)
                
                try:
                    purchase_total += int(item['quantity'])
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
        'purchase_items': purchase_display_data,
        'item_count': purchase_total
    }
    return render_template('view_purchase.html', **context)
