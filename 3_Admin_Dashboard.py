import streamlit as st
from db import get_connection
import datetime

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please log in as admin to access this page.")
    st.stop()
if st.session_state.user["role"] != "admin":
    st.error("You do not have admin privileges.")
    st.stop()

st.title("Admin Dashboard")

# --- Create Poll ---
st.header("Create a New Poll")
with st.form("create_poll"):
    title = st.text_input("Poll Title")
    description = st.text_area("Description")
    # Use date and time input to get full datetime
    start_date = st.date_input("Start Date", value=datetime.date.today())
    start_time = st.time_input("Start Time", value=datetime.datetime.now().time())
    end_date = st.date_input("End Date", value=datetime.date.today())
    end_time = st.time_input("End Time", value=(datetime.datetime.now() + datetime.timedelta(hours=1)).time())
    options = st.text_area("Options (one per line)")
    submitted = st.form_submit_button("Create Poll")
    if submitted and title and options:
        # Combine date and time into datetime strings
        start_datetime = datetime.datetime.combine(start_date, start_time)
        end_datetime = datetime.datetime.combine(end_date, end_time)
        conn = get_connection()
        cursor = conn.cursor()
        try:
            creator_id = st.session_state.user["user_id"]
            cursor.execute(
                "INSERT INTO Polls (title, description, start_time, end_time, creator_id) VALUES (%s, %s, %s, %s, %s)",
                (title, description, start_datetime, end_datetime, creator_id)
            )
            poll_id = cursor.lastrowid
            for opt in options.strip().split('\n'):
                cursor.execute(
                    "INSERT INTO Options (poll_id, option_text) VALUES (%s, %s)",
                    (poll_id, opt.strip())
                )
            conn.commit()
            st.success("Poll created!")
            st.rerun()  # Refresh the page to show updated poll list
        except Exception as e:
            st.error(f"Error creating poll: {e}")
        finally:
            cursor.close()
            conn.close()

# --- List and Delete Polls ---
st.header("Existing Polls")
conn = get_connection()
cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT poll_id, title FROM Polls")
polls = cursor.fetchall()
cursor.close()
conn.close()

if polls:
    poll_titles = [p['title'] for p in polls]
    poll_to_delete = st.selectbox("Select poll to delete", [""] + poll_titles)
    if poll_to_delete and st.button("Delete Selected Poll"):
        poll_id = [p['poll_id'] for p in polls if p['title'] == poll_to_delete][0]
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Polls WHERE poll_id = %s", (poll_id,))
            conn.commit()
            st.success("Poll deleted!")
            st.rerun()  # Refresh the page to update poll list
        except Exception as e:
            st.error(f"Error deleting poll: {e}")
        finally:
            cursor.close()
            conn.close()
else:
    st.info("No polls available.")
