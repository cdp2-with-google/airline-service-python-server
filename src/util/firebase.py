import firebase_admin
from firebase_admin import credentials, firestore

def init_firestore_client():
    cred = credentials.Certificate("resources/firestoreAccountKey.json")
    firebase_admin.initialize_app(cred)
    return firestore.client()

