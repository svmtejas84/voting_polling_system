import streamlit as st
import pandas as pd
from db import get_connection

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please log in to view results.")
    st.stop()

def get_polls():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT poll_id, title FROM Polls")
    polls = cursor.fetchall()
    cursor.close()
    conn.close()
    return polls

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

st.title("Poll Results")

if st.button("🔄 Refresh Results"):
    st.rerun()

polls = get_polls()
if not polls:
    st.info("No polls available.")
else:
    poll_titles = [p['title'] for p in polls]
    poll_choice = st.selectbox("Select a poll", poll_titles)
    poll_id = [p['poll_id'] for p in polls if p['title'] == poll_choice][0]
    results = get_results(poll_id)
    if results:
        df = pd.DataFrame(results)
        st.bar_chart(df.set_index('option_text'))
    else:
        st.info("No votes yet for this poll.")
