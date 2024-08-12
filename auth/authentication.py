import firebase_admin
from firebase_admin import firestore

def is_registered(db, username):
    user_ref = db.collection('users').document(username)
    return user_ref.get().exists

def save_credentials(db, username, password):
    user_ref = db.collection('users').document(username)
    user_ref.set({
        'username': username,
        'password': password
    })

def login_user(db, username, password):
    user_ref = db.collection('users').document(username)
    user_doc = user_ref.get()
    if user_doc.exists:
        return user_doc.to_dict()['password'] == password
    return False