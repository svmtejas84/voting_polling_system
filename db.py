import streamlit as st
import mysql.connector
import hashlib

# --- Database Connection ---
def get_connection():
    db_config = st.secrets["mysql"]
    return mysql.connector.connect(
        host=db_config.host,
        user=db_config.user,
        password=db_config.password,
        database=db_config.database,
        port=int(db_config.port)
    )

# --- Password Hashing ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# --- User Registration ---
def register_user(name, email, password, role):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Users (name, email, password_hash, role) VALUES (%s, %s, %s, %s)",
            (name, email, hash_password(password), role)
        )
        conn.commit()
        return True, "Registration successful!"
    except mysql.connector.IntegrityError:
        return False, "Email already registered."
    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

# --- User Login ---
def login_user(email, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT user_id, name, role, password_hash FROM Users WHERE email=%s", (email,)
    )
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user and user["password_hash"] == hash_password(password):
        return user
    return None

# --- Fetch All Polls ---
def fetch_polls():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Polls")
    polls = cursor.fetchall()
    cursor.close()
    conn.close()
    return polls

# --- Fetch Poll Options ---
def get_poll_options(poll_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT option_id, option_text FROM Options WHERE poll_id = %s", (poll_id,))
    options = cursor.fetchall()
    cursor.close()
    conn.close()
    return options

# --- Check if User Has Voted ---
def has_voted(user_id, poll_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM Votes WHERE user_id=%s AND poll_id=%s", (user_id, poll_id))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

# --- Submit a Vote ---
def submit_vote(user_id, poll_id, option_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Votes (user_id, poll_id, option_id) VALUES (%s, %s, %s)",
            (user_id, poll_id, option_id)
        )
        conn.commit()
        return True, "Vote submitted!"
    except Exception as e:
        return False, "You have already voted in this poll or an error occurred."
    finally:
        cursor.close()
        conn.close()

# --- Create a Poll (Admin) ---
def create_poll(title, description, start_time, end_time, creator_id, options_list):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Polls (title, description, start_time, end_time, creator_id) VALUES (%s, %s, %s, %s, %s)",
            (title, description, start_time, end_time, creator_id)
        )
        poll_id = cursor.lastrowid
        for opt in options_list:
            cursor.execute(
                "INSERT INTO Options (poll_id, option_text) VALUES (%s, %s)",
                (poll_id, opt.strip())
            )
        conn.commit()
        return True, "Poll created!"
    except Exception as e:
        return False, f"Error creating poll: {e}"
    finally:
        cursor.close()
        conn.close()

# --- Delete a Poll (Admin) ---
def delete_poll(poll_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Polls WHERE poll_id = %s", (poll_id,))
        conn.commit()
        return True, "Poll deleted!"
    except Exception as e:
        return False, f"Error deleting poll: {e}"
    finally:
        cursor.close()
        conn.close()

# --- Fetch Poll Results ---
def get_results(poll_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT o.option_text, COUNT(v.vote_id) as votes
        FROM Options o
        LEFT JOIN Votes v ON o.option_id = v.option_id
        WHERE o.poll_id = %s
        GROUP BY o.option_id, o.option_text
        """, (poll_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

# --- Fetch All Poll Titles & IDs ---
def get_polls_titles_ids():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT poll_id, title FROM Polls")
    polls = cursor.fetchall()
    cursor.close()
    conn.close()
    return polls
