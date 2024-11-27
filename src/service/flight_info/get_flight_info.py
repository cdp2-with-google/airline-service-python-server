from ...util.firebase import init_firestore_client
import requests

def get_flight_info():
    """
    :param collection_name: 컬렉션 이름 (string)
    :param field_name: 필드 이름 (string)
    :param operator: 비교 연산자 (string, e.g., '==', '>', '<', '>=', '<=', '!=')
    :param value: 조건 값
    """
    db = init_firestore_client()
    collection_name = "test"
    query = db.collection(collection_name).where("test1", "!=", "null").stream()
    #print(query)
    for doc in query:
        print(f"{doc.id}: {doc.to_dict()}")
        
        
def request_api():
    url = 'http://openapi.airport.co.kr/service/rest/FlightScheduleList/getIflightScheduleList'
    encodingServiceKey = "CLOFRc6QeHPzk206iUaSxpsrv1NIq5JGMBXAVXvnKYh5rUpRNKOadLGr%2BjI%2BibALVFX%2Ba3pLAu35szb21BvLFw%3D%3D"
    decodingServiceKey = "CLOFRc6QeHPzk206iUaSxpsrv1NIq5JGMBXAVXvnKYh5rUpRNKOadLGr+jI+ibALVFX+a3pLAu35szb21BvLFw=="
    params ={'serviceKey' : decodingServiceKey, 'schDate' : '20241128', 'schDeptCityCode' : 'GMP', 'schArrvCityCode' : 'HND', 'schAirLine' : 'NH', 'schFlightNum' : 'NH862' }

    response = requests.get(url, params=params)
    print(response.content)