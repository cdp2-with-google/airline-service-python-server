from ...util.firebase import init_firestore_client
from google.cloud.firestore_v1.base_query import FieldFilter
from datetime import datetime, timedelta

db = init_firestore_client()
collection_name = "flight_info"

def get_flight_info(args):
    """
    :param collection_name: 컬렉션 이름 (string)
    :param field_name: 필드 이름 (string)
    :param operator: 비교 연산자 (string, e.g., '==', '>', '<', '>=', '<=', '!=')
    :param value: 조건 값
    """
    query_res = db.collection(collection_name)\
        .where(filter=FieldFilter("`출발공항`", "==", args["departure_code"]))\
        .where(filter=FieldFilter("`도착공항`", "==", args["destination_code"]))\
        .stream()
    
    data = {
        "date": args["date"],
        "departure": args["departure"],
        "destination": args["destination"],
        "departure_code": args["departure_code"],
        "destination_code": args["destination_code"],
        "list": []
    }
    for doc in query_res:
        print(f"{doc.id}: {doc.to_dict()}")
        doc_dict = doc.to_dict()
        departure_time = doc_dict["출발시간"][0:5]
        arrival_time = doc_dict["도착시간"][0:5]
        data["list"].append({
            "price": doc_dict["price"],
            "flight_time": get_time_gap(departure_time, arrival_time),
            "departure_time": departure_time,
            "arrival_time": arrival_time
        })
    return data


def get_time_gap(time1, time2):
    # time1, time2는 HH:MM 형식의 문자열

    # HH:MM 형식으로 시간 문자열을 datetime 객체로 변환
    fmt = "%H:%M"
    t1 = datetime.strptime(time1, fmt)
    t2 = datetime.strptime(time2, fmt)

    # 시간 간격 계산
    time_difference = t2 - t1 if t2 >= t1 else t2 - t1 + timedelta(days=1)

    # 시간 간격을 HH:MM 형식으로 변환
    total_minutes = int(time_difference.total_seconds() / 60)
    hours, minutes = divmod(total_minutes, 60)
    return f"{hours:02}:{minutes:02}"

# booking_flight에서 사용할 함수 -> 조회되는 값은 하나 뿐이라 가정
# get_specific_flight_id => 명확히 출발, 도착 공항 code와 출발 시간까지 명시돼있어야 함.
def get_specific_fight_info(args):
    print("args : ", args)
    query_res = db.collection(collection_name)\
        .where(filter=FieldFilter("`출발공항`", "==", args["departure_code"]))\
        .where(filter=FieldFilter("`도착공항`", "==", args["destination_code"]))\
        .where(filter=FieldFilter("`출발시간`", "==", args["time"]+":00"))\
        .stream()
    result_list = list(query_res)
    if len(result_list) == 0:
        return None
    return {
        "flight_id":result_list[0].id,
        "data": result_list[0].to_dict()
    }
