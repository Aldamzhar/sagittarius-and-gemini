import firebase_admin
from firebase_admin import credentials, firestore, auth
import streamlit as st

def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(dict(st.secrets["firebase"]))
        firebase_admin.initialize_app(cred)
    else:
        firebase_admin.get_app()

    return firestore.client()
