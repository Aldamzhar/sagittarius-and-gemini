import streamlit as st
from chatbot.chatbot import initialize_model
from chatbot.chat_history import load_chat_sessions

def generate_summary(text):
    model = initialize_model()
    chat = model.start_chat(history=[])
    response = chat.send_message("Summarize the following session of user and AI therapist: " + text)
    return response.text

def save_summary(db, username, session_name, summary, messages):
    summary_ref = db.collection('users').document(username).collection('session_summaries').document(session_name)
    summary_ref.set({
        'summary': summary,
        'messages': messages
    })

def get_summary_and_messages(db, username, session_name):
    summary_ref = db.collection('users').document(username).collection('session_summaries').document(session_name)
    summary_doc = summary_ref.get()
    if summary_doc.exists:
        data = summary_doc.to_dict()
        return data.get('summary'), data.get('messages')
    return None, None

def display_session_summaries(db, username):
    sessions = load_chat_sessions(db, username)
    if sessions:
        for i, session in enumerate(sessions, 1):
            session_name = session['session_id']
            current_messages = [message['parts'] for message in session['messages']]
            summary, stored_messages = get_summary_and_messages(db, username, session_name)
            
            if stored_messages != current_messages:
                session_text = "\n".join(current_messages)
                summary = generate_summary(session_text)
                save_summary(db, username, session_name, summary, current_messages)
            
            st.markdown(f"**Session {i}:**")
            st.write(summary)
    else:
        st.write("No chat sessions available for summarization.")
