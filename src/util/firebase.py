import firebase_admin
from firebase_admin import credentials, firestore

def init_firestore_client():
    if not firebase_admin._apps:  # Firebase 앱이 초기화되지 않은 경우
        cred = credentials.Certificate("resources/firestoreAccountKey.json")
        firebase_admin.initialize_app(cred)
    return firestore.client()
