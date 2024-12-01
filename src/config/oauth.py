from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
import jwt
import datetime
import uuid
import config
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {
    "origins": "http://localhost:3000",
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # 허용할 HTTP 메서드
    "allow_headers": ["Content-Type", "Authorization"],      # 허용할 헤더
    "supports_credentials": True                             # 인증 정보 허용
}})

app.secret_key = os.urandom(24)

# Firestore 초기화
cred = credentials.Certificate(config.FIREBASE_CREDENTIALS_PATH)
initialize_app(cred)
db = firestore.client()

# JWT 비밀키
SECRET_KEY = config.SECRET_KEY

# JWT 생성 함수
def generate_access_token(user_info):
    """
    사용자 정보를 기반으로 JWT Access Token 생성
    """
    # UTC 타임존을 지정한 datetime 객체 생성
    utc_now = datetime.datetime.now(datetime.timezone.utc)

    payload = {
        "iss": "http://127.0.0.1:5000", #서버 주소로 고쳐야 됨
        "sub": user_info["sub"],
        "email": user_info["email"],
        "name": user_info["name"],
        "exp": utc_now + datetime.timedelta(hours=1),  # 1시간 만료
        "iat": utc_now
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def generate_refresh_token():
    """
    UUID를 기반으로 JWT Refresh Token 생성
    """
    # UTC 타임존을 지정한 datetime 객체 생성
    utc_now = datetime.datetime.now(datetime.timezone.utc)

    payload = {
        "iss": "your_server",
        "sub": str(uuid.uuid4()),
        "exp": utc_now + datetime.timedelta(days=30),  # 30일 만료
        "iat": utc_now
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

@app.route('/api/v1/oauth', methods=['POST'])
def oauth_login():
    """
    클라이언트로부터 Google Access Token을 받아 사용자 정보를 저장하고 자체 Access Token 반환
    """
    # 클라이언트에서 전송한 Google Access Token (Social Token)
    social_token = request.json.get('socialToken')

    if not social_token:
        return jsonify({"error": "Social token is missing"}), 400

    try:
        # Google OAuth 토큰 검증 및 사용자 정보 가져오기
        # 예시: PyJWT로 토큰 디코딩 (실제 구현에서는 Google의 tokeninfo 엔드포인트 사용 권장)
        user_info = jwt.decode(social_token, options={"verify_signature": False})  # 임시: 서명 검증 비활성화

        # 사용자 정보 Firestore 저장
        user_ref = db.collection('users').document(user_info['sub'])
        user_ref.set({
            'email': user_info['email'],
            'name': user_info['name'],
            'picture': user_info.get('picture', ''),
            'socialToken': social_token  # 구글 소셜 토큰 저장
        })

        # 자체 Access Token 및 Refresh Token 생성
        access_token = generate_access_token(user_info)
        refresh_token = generate_refresh_token()

        # 클라이언트에 반환
        return jsonify({
            'accessToken': access_token,
            'refreshToken': refresh_token
        })

    except Exception as e:
        return jsonify({"error": f"Token validation failed: {str(e)}"}), 400

if __name__ == '__main__':
    app.run(debug=True)
