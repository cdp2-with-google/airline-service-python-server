from ...util.firebase import build_firestore_client

def get_flight_info():
    """
    :param collection_name: 컬렉션 이름 (string)
    :param field_name: 필드 이름 (string)
    :param operator: 비교 연산자 (string, e.g., '==', '>', '<', '>=', '<=', '!=')
    :param value: 조건 값
    """
    db = build_firestore_client()
    collection_name = "test"
    query = db.collection(collection_name).where("test1", "!=", "null").stream()
    #print(query)
    for doc in query:
        print(f"{doc.id}: {doc.to_dict()}")
        