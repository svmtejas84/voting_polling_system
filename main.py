import streamlit as st
from db import register_user, login_user

st.set_page_config(page_title="Voting & Polling Platform", layout="wide")

if "user" not in st.session_state:
    st.session_state.user = None

def show_login():
    st.header("Login")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        if submit:
            user = login_user(email, password)
            if user:
                st.session_state.user = user
                st.success(f"Welcome, {user['name']} ({user['role']})!")
                st.rerun()
            else:
                st.error("Invalid credentials.")

def show_register():
    st.header("Register")
    with st.form("register_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["student", "admin"])
        submit = st.form_submit_button("Register")
        if submit:
            ok, msg = register_user(name, email, password, role)
            if ok:
                st.success(msg)
            else:
                st.error(msg)

if st.session_state.user:
    st.sidebar.success(f"Logged in as: {st.session_state.user['name']} ({st.session_state.user['role']})")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()
    st.title("Welcome to the Smart Voting & Polling Platform!")
    st.write("Use the sidebar to navigate.")
else:
    tab1, tab2 = st.tabs(["Login", "Register"])
    with tab1:
        show_login()
    with tab2:
        show_register()
