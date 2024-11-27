from ...util.firebase import build_firestore_client

# def get_flight_info():
db = build_firestore_client()
collection_name = "test"
docs = db.collection(collection_name).stream()
print(docs)
for doc in docs:
    print(f"{doc.id}: {doc.to_dict()}")
        
