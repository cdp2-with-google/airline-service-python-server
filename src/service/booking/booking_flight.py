from ...util.firebase import init_firestore_client

def book_flight():
    db = init_firestore_client()
    collection_name = "test"
    document_id = "doc1"
    data = {
        'name': 'John',
        'age': 30,
        'email': 'john@example.com'
    }
    
    doc_ref = db.collection(collection_name).document(document_id)
    doc_ref.set(data)
    
    print('데이터가 성공적으로 추가되었습니다.')
    