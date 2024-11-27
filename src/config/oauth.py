from flask import Flask, request, redirect, session, jsonify
from google_auth_oauthlib.flow import Flow
from firebase_admin import credentials, firestore, initialize_app
import os
import config

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Firestore 초기화
cred = credentials.Certificate(config.FIREBASE_CREDENTIALS_PATH)
initialize_app(cred)
db = firestore.client()

# OAuth 2.0 Flow 초기화
flow = Flow.from_client_secrets_file(
    'src/config/client_secret_965998489425-b14jbag85kh6g0cog4ro3kd5jjf9lpql.apps.googleusercontent.com.json',
    scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'],
    redirect_uri='https://service-client-965998489425.asia-northeast1.run.app'
)

@app.route('/api/v1/oauth', methods=['POST'])
def oauth_login():
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    user_info = credentials.id_token

    # 사용자 정보 저장 (Firestore)
    user_ref = db.collection('users').document(user_info['sub'])
    user_ref.set({
        'email': user_info['email'],
        'name': user_info['name'],
        'picture': user_info['picture'],
        'accessToken': credentials.token,
        'refreshToken': credentials.refresh_token
    })

    # 토큰을 프론트엔드로 반환
    return jsonify({
        'accessToken': credentials.token,
        'refreshToken': credentials.refresh_token
    })

if __name__ == '__main__':
    app.run(debug=True)