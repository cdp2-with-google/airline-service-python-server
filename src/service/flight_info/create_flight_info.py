from ...util.firebase import init_firestore_client
import pandas as pd

def create_flight_info():
    db = init_firestore_client()
    # 엑셀 파일 읽기
    df = pd.read_excel("resources/flight_info.xlsx")
    
    # "flight_info" 컬렉션 지정
    collection_ref = db.collection("flight_info")
    
    # 각 행을 Firestore에 저장
    for _, row in df.iterrows():
        # a열(순번)을 문서 ID로 설정
        doc_id = str(row["순번"])
        
        # 나머지 열 데이터를 딕셔너리로 변환
        data = {
            "항공사": str(row["항공사"]),
            "운항편명": str(row["운항편명"]),
            "출발공항": str(row["출발공항"]),
            "도착공항": str(row["도착공항"]),
            "출발시간": str(row["출발시간"]),
            "도착시간": str(row["도착시간"])
        }
        
        # Firestore에 저장
        collection_ref.document(doc_id).set(data)
        print(f"Document {doc_id} uploaded successfully.")
