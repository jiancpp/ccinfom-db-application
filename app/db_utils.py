from app.config import DB_HOST, DB_USER, DB_PASS, DB_NAME
from flask import request
import mysql.connector

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

def execute_modified_insert(sql, params=()):
    conn = None
    cursor = None
    last_id = None

    try:
        conn = get_conn()
        cursor = conn.cursor() 
        cursor.execute(sql, params)
        conn.commit()
        last_id = cursor.lastrowid  # <--- THIS IS THE KEY CHANGE
        
    except Exception as e:
        # In a real app, you should log this error
        print(f"Error executing insert: {e}")
        if conn:
            conn.rollback() # Ensure rollback on error
            
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    # Return the ID, which will be None if the insert failed or the table has no auto-increment key
    return last_id

def get_updated_value(key, current_db_value):
        submitted_value = request.form.get(key)
        if submitted_value is None or submitted_value.strip() == '':
            return current_db_value
            
        return submitted_value.strip()