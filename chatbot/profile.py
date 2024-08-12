import streamlit as st
from firebase_admin import auth

def move_user_data(db, old_username, new_username):
    old_sessions_ref = db.collection('users').document(old_username).collection('chat_sessions')
    new_sessions_ref = db.collection('users').document(new_username).collection('chat_sessions')
    
    sessions = old_sessions_ref.stream()
    for session in sessions:
        session_data = session.to_dict()
        new_sessions_ref.document(session.id).set(session_data)
    
    old_summaries_ref = db.collection('users').document(old_username).collection('session_summaries')
    new_summaries_ref = db.collection('users').document(new_username).collection('session_summaries')
    
    summaries = old_summaries_ref.stream()
    for summary in summaries:
        summary_data = summary.to_dict()
        new_summaries_ref.document(summary.id).set(summary_data)
    
    old_sessions_ref.parent.delete()
    old_summaries_ref.parent.delete()

def update_user_info(db, old_username, new_username, new_password):
    user_ref = db.collection('users').document(old_username)
    user_doc = user_ref.get()
    
    if user_doc.exists:
        user_ref.update({
            'username': new_username,
            'password': new_password
        })
        
        if old_username != new_username:
            move_user_data(db, old_username, new_username)
            new_user_ref = db.collection('users').document(new_username)
            new_user_ref.set(user_doc.to_dict())
            user_ref.delete()
        
        st.session_state.username = new_username
        st.session_state.password = new_password
        st.success("Profile updated successfully!")
    else:
        st.error("User does not exist!")

def display_profile_page(db):
    st.header("Profile")
    current_username = st.session_state.username
    current_password = st.session_state.password
    
    new_username = st.text_input("New Username", value=current_username)
    new_password = st.text_input("New Password", value=current_password, type="password")
    
    if st.button("Save Changes"):
        update_user_info(db, current_username, new_username, new_password)

    if st.button("Back to Chat"):
        st.session_state.page = 'Chat'
        st.rerun()
