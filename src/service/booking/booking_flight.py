import random
from ...util.firebase import init_firestore_client
from ..flight_info.get_flight_info import get_specific_fight_info
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from ...config.config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET,SECRET_KEY
import pytz
from datetime import datetime

def format_event_time(date, time):
    # 한국 시간(KST) 타임존 설정
    kst = pytz.timezone('Asia/Seoul')

    # 날짜와 시간을 하나로 합침 (예: "2024-12-15 14:30")
    date_time = f"{date} {time}"
    
    # 문자열을 datetime 객체로 변환
    local_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M")
    
    # 한국 시간대(KST)로 변환
    local_time = kst.localize(local_time)
    
    # ISO 8601 형식으로 변환
    return local_time.isoformat()
    
def get_social_token(args):
    db = init_firestore_client()
    collection_name = "users"
    
    # 이메일로 해당 사용자 찾기
    query_res = db.collection(collection_name).where("email", "==", args["email"]).limit(1).stream()

    # 결과에서 첫 번째 문서 가져오기
    # 첫 번째 문서 또는 없으면 None
    doc = next(query_res, None) 

    if doc:
        user_data = doc.to_dict()
        return user_data.get("socialToken", None)  
    return None

# Google Calendar Transaction
def add_event_to_calendar(user_data, flight_data):

    departure_time = format_event_time(flight_data['date'], flight_data['departure_time'])
    arrival_time = format_event_time(flight_data['date'], flight_data['arrival_time'])

    socialToken = get_social_token(user_data)
    # Google Calendar API 클라이언트
    credentials = Credentials(
        token=socialToken,
    )
    service = build('calendar', 'v3', credentials=credentials)

    event = {
        'summary': f"{flight_data['name']} 님의 항공편 예약: {flight_data['departure_code']} -> {flight_data['destination_code']} ({flight_data['flight_id']})",
        'description': (
            f"Passenger: {flight_data['name']} (Age: {flight_data['age']})\n"
            f"Email: {flight_data['email']}\n"
            f"Flight Date: {flight_data['date']}\n"
            f"Gate: {flight_data['gate']}, Seat: {flight_data['seat_number']}\n"
            f"Class: {flight_data['seat_class']}"
        ),
        'start': {
            'dateTime': departure_time,
            'timeZone': 'Asia/Seoul',  # 한국 시간대(KST)로 설정
        },
        'end': {
            'dateTime': arrival_time,
            'timeZone': 'Asia/Seoul',
        },
        # 'start': {
        #     'dateTime': '2024-12-22T09:00:00',
        #     'timeZone': 'Asia/Seoul',
        # },
        # 'end': {
        #     'dateTime': '2024-12-22T17:00:00',
        #     'timeZone': 'Asia/Seoul',
        # },
    }

    # Google Calendar에 이벤트 생성
    event_result = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Event created: {event_result.get('htmlLink')}")
    
    

def book_flight(args, user_data):
    db = init_firestore_client()
    collection_name = "booking_flight"

    # 랜덤 게이트 번호 생성 (1 ~ 30)
    gate = random.randint(1, 30)

    # 랜덤 좌석 번호 생성 (1 ~ 30 + A ~ H)
    seat_number = f"{random.randint(1, 30)}{random.choice('ABCDEFGH')}"

    # 랜덤 클래스 선택 (이코노미, 비즈니스, 퍼스트)
    seat_class = random.choice(["이코노미", "비즈니스", "퍼스트"])

    # 항공편 정보 가져와 id 추출
    flight_info = get_specific_fight_info({
        "departure_code": args["departure_code"],
        "destination_code": args["destination_code"],
        "time": args["time"]
    })
    if (flight_info is None):
        return None
    flight_id = flight_info["flight_id"]
    flight_data = flight_info["data"]

    name = user_data.get("name")
    email = user_data.get("email")

    data = {
        "airline": flight_data["항공사"],
        "departure_code": flight_data["출발공항"],
        "destination_code": flight_data["도착공항"],
        "flight_id": flight_id,
        "gate": gate,
        "seat_number": seat_number,
        "seat_class": seat_class,
        "name": name,
        "age": 25,
        "email": email,
        "date": args["date"],
        "departure_time": flight_data["출발시간"][0:5],
		"arrival_time": flight_data["도착시간"][0:5],
    }

    # Firestore에 데이터 추가
    doc_ref = db.collection(collection_name).document()
    doc_ref.set(data)
    print("데이터가 성공적으로 추가되었습니다.")

    add_event_to_calendar(user_data, data)

    return {
        "airline": flight_data["항공사"],
        "departure_code": flight_data["출발공항"],
        "destination_code": flight_data["도착공항"],
        "gate": gate,
        "seat": seat_number,
        "class": seat_class,
        "name": name,
        "date": args["date"],
        "departure_time": flight_data["출발시간"][0:5],
		"arrival_time": flight_data["도착시간"][0:5],
        "price": flight_data["price"]
    }
