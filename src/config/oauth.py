from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
import jwt
import datetime
import uuid
from src.config.config import GOOGLE_CLIENT_ID, SECRET_KEY
from src.settings import SERVER_URL
import requests
from flask_cors import CORS
from jwt import PyJWTError

# JWT 비밀키
SECRET_KEY = SECRET_KEY

# Google Access Token을 사용하여 사용자 정보 가져오기
def verify_google_access_token(access_token):
    try:
        response = requests.get(
            'https://www.googleapis.com/oauth2/v1/userinfo',
            params={'access_token': access_token}
        )
        
        if response.status_code == 200:
            user_info = response.json()
            # print("User info from Google:", user_info) # 디버깅용
            return user_info
        else:
            raise Exception("Failed to fetch user information from Google")
    
    except Exception as e:
        raise Exception(f"Access token validation failed: {e}")

# JWT 생성 함수
def generate_access_token(user_info):
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    payload = {
        "iss": SERVER_URL,  # 서버 URI
        "sub": user_info["id"],
        "email": user_info["email"],
        "name": user_info["name"],
        "exp": utc_now + datetime.timedelta(hours=1),  # 1시간 만료
        "iat": utc_now
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def generate_refresh_token():
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    payload = {
        "iss": SERVER_URL,
        "sub": str(uuid.uuid4()),
        "exp": utc_now + datetime.timedelta(days=30),  # 30일 만료
        "iat": utc_now
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")