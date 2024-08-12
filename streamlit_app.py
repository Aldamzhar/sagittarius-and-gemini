import streamlit as st
from datetime import datetime, timedelta
from auth.firebase_setup import initialize_firebase
from auth.authentication import is_registered, save_credentials, login_user
from chatbot.chatbot import initialize_model, run_chatbot
from chatbot.chat_history import save_chat_session, display_chat_sessions, load_chat_sessions
from chatbot.sentiment_analysis import display_sentiment_analysis
from chatbot.session_summaries import display_session_summaries
from chatbot.profile import display_profile_page

db = initialize_firebase()

model = initialize_model()

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'session_start_time' not in st.session_state:
    st.session_state.session_start_time = None

if 'username' not in st.session_state:
    st.session_state.username = None

if 'password' not in st.session_state:
    st.session_state.password = None

if 'show_login' not in st.session_state:
    st.session_state.show_login = False

if 'page' not in st.session_state:
    st.session_state.page = 'Chat'

if st.session_state.session_start_time:
    session_duration = datetime.now() - st.session_state.session_start_time
    if session_duration > timedelta(minutes=30):
        st.session_state.authenticated = False
        st.session_state.session_start_time = None
        st.session_state.username = None
        st.session_state.password = None

if st.session_state.username and st.session_state.password and not st.session_state.authenticated:
    if login_user(db, st.session_state.username, st.session_state.password):
        st.session_state.authenticated = True
        st.session_state.session_start_time = datetime.now()

def logout():
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.password = None
    st.session_state.page = 'Login'
    st.rerun()

if not st.session_state.authenticated:
    if st.session_state.show_login:
        st.markdown("### Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if login_user(db, username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.password = password
                st.session_state.session_start_time = datetime.now()
                st.success("Successfully logged in!")
                st.rerun()
            else:
                st.error("Incorrect username or password!")
        if st.button("Don't have an account? Register here."):
            st.session_state.show_login = False
            st.rerun()
    else:
        st.markdown("### Register")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Register"):
            if not is_registered(db, username):
                save_credentials(db, username, password)
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.password = password
                st.session_state.session_start_time = datetime.now()
                st.success("Successfully registered!")
                st.rerun()
            else:
                st.error("User with this username already exists. Please try logging in or choose a different username.")
        if st.button("Already have an account? Login here."):
            st.session_state.show_login = True
            st.rerun()

if st.session_state.authenticated:
    if st.session_state.page == 'Chat':
        if st.sidebar.button('Go to Profile'):
            st.session_state.page = 'Profile'
            st.rerun()

        if st.sidebar.button('Go to Sentiment Analysis'):
            st.session_state.page = 'Sentiment'
            st.rerun()

        if st.sidebar.button('Go to Session Summaries'):
            st.session_state.page = 'Summaries'
            st.rerun()

        if st.sidebar.button('Logout'):
            logout()

        run_chatbot(model)
        display_chat_sessions(db)
        save_chat_session(db, st.session_state.username, st.session_state.messages)

    elif st.session_state.page == 'Profile':
        display_profile_page(db)

    elif st.session_state.page == 'Sentiment':
        st.header("Sentiment Analysis Across Sessions")
        display_sentiment_analysis(db, st.session_state.username)
        
        if st.button('Back to Chat'):
            st.session_state.page = 'Chat'
            st.rerun()

    elif st.session_state.page == 'Summaries':
        st.header("Session Summaries")
        display_session_summaries(db, st.session_state.username)

        if st.button('Back to Chat'):
            st.session_state.page = 'Chat'
            st.rerun()
