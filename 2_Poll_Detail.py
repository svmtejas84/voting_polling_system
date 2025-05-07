import streamlit as st
from db import get_connection

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please log in to vote.")
    st.stop()

def get_polls():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT poll_id, title FROM Polls")
    polls = cursor.fetchall()
    cursor.close()
    conn.close()
    return polls

def get_poll_options(poll_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT option_id, option_text FROM Options WHERE poll_id = %s", (poll_id,))
    options = cursor.fetchall()
    cursor.close()
    conn.close()
    return options

def has_voted(user_id, poll_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM Votes WHERE user_id=%s AND poll_id=%s", (user_id, poll_id))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

def submit_vote(user_id, poll_id, option_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Votes (user_id, poll_id, option_id) VALUES (%s, %s, %s)",
            (user_id, poll_id, option_id)
        )
        conn.commit()
        st.success("Vote submitted!")
        st.rerun()  # Refresh to reflect the voting status
    except Exception as e:
        st.error("You have already voted in this poll or an error occurred.")
    finally:
        cursor.close()
        conn.close()

st.title("Vote in a Poll")

polls = get_polls()
if not polls:
    st.info("No polls available.")
else:
    poll_titles = [p['title'] for p in polls]
    poll_choice = st.selectbox("Select a poll", poll_titles)
    poll_id = [p['poll_id'] for p in polls if p['title'] == poll_choice][0]
    options = get_poll_options(poll_id)
    if options:
        option_texts = [o['option_text'] for o in options]
        selected_option = st.radio("Choose an option", option_texts)
        option_id = [o['option_id'] for o in options if o['option_text'] == selected_option][0]
        user_id = st.session_state.user["user_id"]
        if has_voted(user_id, poll_id):
            st.info("You have already voted in this poll.")
        else:
            if st.button("Submit Vote"):
                submit_vote(user_id, poll_id, option_id)
    else:
        st.warning("No options for this poll.")
