from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import time
import json
from datetime import datetime
from src.service.tool.react import send_chat_message
from src.config.oauth import verify_google_access_token,generate_access_token, generate_refresh_token
from src.util.firebase import init_firestore_client
from src.config.config import SECRET_KEY
import jwt

app = Flask(__name__)
CORS(app)

# Firestore 초기화
db = init_firestore_client()

@app.route('/api/v1/oauth', methods=['POST'])
def oauth_login():
    social_token = request.json.get('socialToken')
    if not social_token:
        return jsonify({"error": "Social token is missing"}), 400

    try:
        # Google Access Token으로 user_info 가져오기
        user_info = verify_google_access_token(social_token)

        # Firestore 저장 (user_info)
        user_ref = db.collection('users').document(user_info['id'])
        user_ref.set({
            'email': user_info['email'],
            'name': user_info['name'],
            'picture': user_info.get('picture', ''),
            'socialToken': social_token
        })
        
        # 자체 Access Token 및 Refresh Token 생성
        access_token = generate_access_token(user_info)
        refresh_token = generate_refresh_token()

        return jsonify({
            'accessToken': access_token,
            'refreshToken': refresh_token
        })

    except Exception as e:
        print(f"Error occurred: {e}")  # 예외 메시지 출력
        return jsonify({"error": f"Token validation failed: {str(e)}"}), 400

# Memory DB
conversations = {}
conversation_id_list = []
new_conversation_id = 0

def make_title(s, length=15):
    if len(s) > length:
        return s[:length] + "..."
    return s

def get_concatenated_messages(conversation_id):
    # pairing 배열 가져오기
    pairing = conversations[conversation_id].get("pairing", [])
    # 배열의 마지막 두 개 가져오기 (최대 두 개만)
    last_two = pairing[-2:]  # 배열 크기가 3보다 작으면 가능한 만큼만 반환
    # "request_message"와 "response_message"를 추출해 \n으로 구분해 문자열로 이어 붙이기
    result = "\n".join(
        f"{item.get('request_message', '')}\n{item.get('response_message', '')}" 
        for item in last_two
    )
    return result

# GET /conversations/id-list
@app.route('/conversations/id-list', methods=['GET'])
def get_id_list():
    return jsonify({"list": conversation_id_list})

# GET /conversations/{conversation_id}
@app.route('/conversations/<int:conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    conversation = conversations.get(conversation_id)
    if conversation:
        return jsonify(conversation)
    else:
        return jsonify({"error": "Conversation not found"}), 404

# accessToken 검증
def verify_access_token(token) :
    try:
        # JWT 토큰 검증
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload # 유효한 토큰이면
    except jwt.ExpiredSignatureError:
        # access Token 갱신하는 로직 들어가야함
        raise Exception("Access token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid access token")
    
# POST /conversations
@app.route('/conversations', methods=['POST'])
def mvp_create_conversation():

    # token 검증하고 사용자 정보 가져오는 로직 시작
    access_token = request.headers.get('auth') # Header의 Auth에 있는 accessToken 가져오기
    # refresh_token은 필요 없을 것 같은데 혹시 사용할까봐 추가해둠
    refresh_token = request.headers.get('refresh') # Header의 Refresh에 있는 refreshToken 가져오기

    if not access_token:
        return jsonify({"error": 'Access token is missing'}), 401
    
    try:
        # accessToken 검증하고 user_info 가져오기
        user_info = verify_access_token(access_token)
        user_name = user_info.get('name')
        user_email = user_info.get('email')

        user_data = {
            # "accessToken" : access_token,
            # "refreshToken" : refresh_token,
            "name" : user_name,
            "email": user_email
        }

    except Exception as e:
        return jsonify({"error": str(e)}), 400

    #######################
    data = request.get_json()

    # 요청으로부터 필요 데이터 추출
    conversation_id = data.get('data', {}).get('conversation_id', 0)
    question = data.get('data', {}).get('question', None)
    engine = data.get('data', {}).get('engine', None)

    # error
    if (engine is None):
        return jsonify({"error": "Engine is not specified"}), 404

    # 기존 대화가 없으면 새로 생성
    if conversation_id is None:
        global new_conversation_id
        conversation_id = new_conversation_id
        new_conversation_id += 1
        title = make_title(question)   # 질문 앞 15글자 잘라서 title로 지정
        conversation_id_list.append({
            "conversation_id": conversation_id,
            "title": title
        })
        conversations[conversation_id] = {
            "title": title,
            "engine": engine,
            "create_time": datetime.now(),
            "update_time": datetime.now(),
            "pairing": []
        }
    elif conversation_id not in conversations:
        return jsonify({"error": "Conversation not found"}), 404

    # 이전 질문답변 세개 정도를 question에 추가하기
    question_to_process = get_concatenated_messages(conversation_id) + "\n-----Previous conversation to refer to -----\n" + question

    # 답변 생성 및 저장
    response = send_chat_message(question_to_process, user_data)  # 여기를 우리가 만든 모델에서 받아오는 부분
    create_time = datetime.now()
    answer = response["answer"]
    response["conversation_id"] = conversation_id
    response["title"] = conversations[conversation_id]["title"]
    response["create_time"] = create_time

    # 요청 메시지와 응답 메시지 저장
    conversation_data = {
        "id": len(conversations[conversation_id]['pairing']),
        "request_message": question,
        "response_message": answer,
        "create_time": create_time,
        "response_type": response["response_type"],
        "data": response["data"]
    }
    conversations[conversation_id]['pairing'].append(conversation_data)

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
