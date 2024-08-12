import streamlit as st
from datetime import datetime

def save_chat_session(db, username, messages):
    if messages:
        session_name = " ".join(messages[0]['parts'].split()[:5]) if messages else "New Session"
        session_ref = db.collection('users').document(username).collection('chat_sessions').document(session_name)
        session_ref.set({
            'timestamp': datetime.now(),
            'messages': messages
        })

def load_chat_sessions(db, username):
    sessions = db.collection('users').document(username).collection('chat_sessions').order_by('timestamp').stream()
    session_list = []
    for session in sessions:
        session_data = session.to_dict()
        session_data['session_id'] = session.id
        session_list.append(session_data)
    return session_list

def display_chat_sessions(db):
    if 'username' in st.session_state:
        st.sidebar.markdown("### Chat History")
        
        if st.sidebar.button("New Chat"):
            st.session_state.messages = []
            st.rerun()

        sessions = load_chat_sessions(db, st.session_state.username)
        if sessions:
            for session in sessions:
                session_name = session['session_id']
                session_time = session['timestamp'].strftime("%d.%m.%Y %H:%M:%S")
                if st.sidebar.button(f"{session_name} ({session_time})"):
                    st.session_state.messages = session['messages']
                    st.rerun()
