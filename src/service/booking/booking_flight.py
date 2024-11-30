import random
from ...util.firebase import init_firestore_client

def book_flight(args):
    db = init_firestore_client()
    collection_name = "booking_flight"

    # 랜덤 게이트 번호 생성 (1 ~ 30)
    gate = random.randint(1, 30)

    # 랜덤 좌석 번호 생성 (1 ~ 30 + A ~ H)
    seat_number = f"{random.randint(1, 30)}{random.choice('ABCDEFGH')}"

    # 랜덤 클래스 선택 (이코노미, 비즈니스, 퍼스트)
    seat_class = random.choice(['이코노미', '비즈니스', '퍼스트'])

    data = {
        'name': 'John',
        'age': 30,
        'email': 'john@example.com',
        'departure': args["departure"],
        'departure_code': args["departure_code"],
        'destination': args["destination"],
        'destination_code': args["destination_code"],
        'date': args["date"],
        'time': args["time"],
        'gate': gate,
        'seat_number': seat_number,
        'seat_class': seat_class
    }

    # Firestore에 데이터 추가
    doc_ref = db.collection(collection_name).document()
    doc_ref.set(data)

    print('데이터가 성공적으로 추가되었습니다.')
