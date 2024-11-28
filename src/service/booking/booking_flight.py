from ...util.firebase import init_firestore_client

def book_flight(args):
    db = init_firestore_client()
    collection_name = "booking_flight"
    data = {
        'name': 'John',
        'age': 30,
        'email': 'john@example.com',
        'departure': args["departure"],
        'departure_code': args["departure_code"],
        'destination': args["destination"],
        'destination_code': args["destination_code"],
        'data': args["date"],
        'time': args["time"]
    }
    
    doc_ref = db.collection(collection_name).document()
    doc_ref.set(data)
    
    print('데이터가 성공적으로 추가되었습니다.')
    