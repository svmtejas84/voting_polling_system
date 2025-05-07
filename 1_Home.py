import streamlit as st
from db import get_connection

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please log in to view polls.")
    st.stop()

st.title("Available Polls")

conn = get_connection()
cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT * FROM Polls")
polls = cursor.fetchall()
cursor.close()
conn.close()

if not polls:
    st.info("No polls available.")
else:
    for poll in polls:
        st.subheader(poll['title'])
        st.write(poll['description'])
        st.write(f"Start: {poll['start_time']} | End: {poll['end_time']}")
        st.write("---")
