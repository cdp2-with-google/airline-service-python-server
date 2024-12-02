import random
from ...util.firebase import init_firestore_client
from ..flight_info.get_flight_info import get_specific_fight_info

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
        "name": name,
        "age": 30,
        "email": email,
        "flight_id": flight_id,
        "date": args["date"],
        "gate": gate,
        "seat_number": seat_number,
        "seat_class": seat_class
    }

    # Firestore에 데이터 추가
    doc_ref = db.collection(collection_name).document()
    doc_ref.set(data)

    print("데이터가 성공적으로 추가되었습니다.")
    return {
        "airline": flight_data["항공사"],
        "departure_code": flight_data["출발공항"],
        "destination_code": flight_data["도착공항"],
        "gate": gate,
        "class": seat_class,
        "name": name,
        "date": args["date"],
        "seat": seat_number,
        "departure_time": flight_data["출발시간"][0:5],
		"arrival_time": flight_data["도착시간"][0:5]
    }
