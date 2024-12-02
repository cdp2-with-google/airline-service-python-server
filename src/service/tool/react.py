import requests
from vertexai.generative_models import (
    FunctionDeclaration,
    GenerationConfig,
    GenerativeModel,
    Part,
    Tool,
)
from ..rag.vertex_ai_search import search_pdf
from datetime import datetime
from ..flight_info.get_flight_info import get_flight_info
from ..booking.booking_flight import book_flight


def delcare_functions() -> Tool:
    # 항공사 운송 약관(탑승 수속, 수하물 규정 등)을 조회
    get_airline_policy = FunctionDeclaration(
        name="get_airline_policy",  # python에서 처리해야하는 함수는 뒤에 _python postfix
        description="Retrieve airlilne policies sush as baggage rules",
        parameters={
            "type": "object",
            "properties": {
                "airline_name": {"type": "string", "description": "The name of the airline name of the policy to be retrieved."},
            },
            "required": ["airline_name"]
        },
    )

    # 공항 정책(환승 규정, 편의 시설 위치 등)을 조회
    get_airport_policy = FunctionDeclaration(
        name="get_airport_policy",
        description="Retrieve airport policies",
        parameters={
            "type": "object",
            "properties": {
                "airport_name": {
                    "type": "string",
                    "description": "The name of the airport name of the policy to be retrieved."
                }
            },
            "required": ["airport_name"]
        }
    )

    # 항공편 정보 조회
    get_flight_information = FunctionDeclaration(
        name="get_flight_information",
        description="Retrieve flight detail informations",
        parameters={
            "type": "object",
            "properties": {
                # "airline_name": {"type": "string", "description": "The name of the airline of the flight to be retrieved."},
                "departure": {"type": "string", "description": "The name of the departure airport of the flight to be retrieved."},
                "destination": {"type": "string", "description": "The name of the destination airport of the flight to be retrieved."},
                "departure_code": {"type": "string", "description": "The code of the departure airport of the flight to be retrieved."},
                "destination_code": {"type": "string", "description": "The code of the destination airport of the flight to be retrieved."},
                "date": {"type": "string", "format": "date", "description": "The departure date of the flight."},
            },
            "required": ["departure", "destination", "departure_code", "destination_code", "date"]
        },
    )

    # 항공편 예약
    book_flight = FunctionDeclaration(
        name="book_flight",
        description="Book a flight requested by the user",
        parameters={
            "type": "object",
            "properties": {
                # "airline_name": {"type": "string", "description": "The name of the airline for the flight to reserve."},
                "departure": {"type": "string", "description": "The name of the departure airport for the flight to reserve."},
                "destination": {"type": "string", "description": "The name of the destination airport for the flight to reserve."},
                "departure_code": {"type": "string", "description": "The code of the departure airport of the flight to reserve."},
                "destination_code": {"type": "string", "description": "The code of the destination airport of the flight to reserve."},
                "date": {"type": "string", "format": "date", "description": "The departure date of the flight to reserve in format YYYY-MM-DD."},
                "time": {"type": "string", "description": "The departure time of the flight to reserve in format HH:MM."},
            },
            "required": ["departure", "destination", "departure_code", "destination_code", "date", "time"]
        },
    )

    flight_tool = Tool(
        function_declarations=[
            # get_flight_fare_info,
            get_airline_policy,
            # get_airport_policy,
            get_flight_information,
            book_flight,
        ],
    )
    return flight_tool

def handle_airline_policy(prompt, args):
    plain_text = search_pdf(prompt)
    return {
        "response_type": "plain_text",
        "answer": plain_text,
        "data": None
    }

def handle_flight_information(prompt, args):
    flight_info = get_flight_info(args)
    return {
        "response_type": "get_flight_info",
        "answer": str(flight_info),
        "data": flight_info
    }

def handle_booking(prompt, args):
    booking_result = book_flight(args)
    if (booking_result is None):
        return {
            "response_type": "plain_text",
            "answer": "없는 비행 일정입니다. 정확한 날짜와 시간을 다시 알려주세요.",
            "data": None
        }
    return {
        "response_type": "book_flight",
        "answer": str(booking_result),
        "data": booking_result
    }

operations = {
    "get_airline_policy": handle_airline_policy,
    "get_flight_information": handle_flight_information,
    "book_flight": handle_booking
}

def send_chat_message(prompt:str, user_data: dict) -> str:
    # (멘토님 추천) Gemini 활용 사전 질문 정제 필요? (ex. 나리타-도쿄 못 찾는 경우 등)
    # 기존 context 유지 위해 대화 내역 가져와서 붙이는거 필요?

    flight_tool = delcare_functions()
    system_instruction = f"""
    system_instruction ="Analyze the user's request and find the appropriate function and its all required properties.
    There are 3 functions, get_airline_policy, get_flight_information, and book_flight.

    <example-get_airline_policy>
    User prompt : Can I take a knife on board the Korean Air flight?
    Predicted Tool : flight_tool
    Predicted Function : get_airline_policy
    Function parameters : {{"airline_name": "Koeran Air"}}
    </example-get_airline_policy>
    <example-get_airline_policy>
    User prompt: What is the baggage allowance for Emirates economy class?
    Predicted Tool: flight_tool
    Predicted Function: get_airline_policy
    Function parameters: {{"airline_name": "Emirates"}}
    </example-get_airline_policy>

    <example-get_flight_information>
    User prompt: I want to know the schedule of the flights departing from Incheon to Tokyo.
    Predicted Tool: None (Need more information because there is no exact date to be retrieved)
    Predicted Function: None (Need more information because there is no exact date to be retrieved)
    Answer: "Give me more informations about date."
    </example-get_flight_information>
    <example-get_flight_information>
    User prompt: I want to know the schedule of the flights departing from Incheon Airport to Narita Airport tomorrow.
    Predicted Tool: flight_tool
    Predicted Function: get_flight_information
    Function parameters: {{"departure": "Incheon", "destination": "Narita", "departure_code": "ICN", "destination_code": "NRT", "date": "YYYY-MM-DD"}} (You must replace "date" with user provided date value)
    </example-get_flight_information>
    <example-get_flight_information>
    User prompt: I want to know the schedule of the flights departing from Incheon to Tokyo tomorrow.
    Predicted Tool: None (Need more information because there is no exact airport name to be retrieved)
    Predicted Function: None (Need more information because there is no exact airport name to be retrieved)
    Answer: "Near by tokyo there are several airports. Which one you want to use? Narita Airport or Haneda Airport?"
    </example-get_flight_information>

    <example-book_flight>
    User prompt: Can I book a flight from Narita to San Francisco?
    Predicted Tool: None (Need more information because there is no exact date and time to reserve)
    Predicted Function: None (Need more information because there is no exact date and time to reserve)
    Answer: "Of course! When do you want to depart? Let me know exact date and time."
    </example-book_flight>
    <example-book_flight>
    User prompt: Can I book a flight from Narita to San Francisco next Friday on 6PM?
    Predicted Tool: flight_tool
    Predicted Function: book_flight
    Function parameters: {{"departure": "Narita", "destination": "San Francisco", "departure_code": "NRT", "destination_code": "SFO", "date": "YYYY-MM-DD", "time": "HH:MM"}} (You must replace date and time with user provided date and time value)
    </example-book_flight>

    <addtional information>
    Date of today : {datetime.today().strftime('%Y-%m-%d')}
    </additional information>

    Follow below instruction strictly.
    1. If the user prompt is enough to set up a function and put a value in the properties, don't ask any additional questions.
    2. If you are unsure which function to use or properties to assign, ask the user for more information.
        2-1. Don't answer the question directly, just (1)find the appropriate function or (2)ask about the additional information you need if you can't find the right function or properties in natural language.
        2-2. Don't use or ask Airport IATA code when asking more information, use Airport name instead.
        2-3. Don't ask about information you can infer.
        2-4. Answer in the language of the user question.
    """
    
    model = GenerativeModel(
        "gemini-1.5-pro-002",
        generation_config=GenerationConfig(temperature=0),
        tools=[flight_tool],
        system_instruction=system_instruction
    )
    chat = model.start_chat()

    # Gemini로 채팅 메시지 보내기
    llm_response = chat.send_message(prompt).candidates[0].content.parts[0]
    print("response => ", llm_response)

    # 함수 호출의 응답에서 값 추출
    if (llm_response.function_call is not None):
        function_args = llm_response.function_call.args
        function_name = llm_response.function_call.name
        
        if (function_name == 'book_flight'):
            response = operations[function_name](prompt, function_args, user_data)
        else:
            response = operations[function_name](prompt, function_args)
    else:
        response = {
            "response_type": "plain_text",
            "answer": llm_response.text,
            "data": None
        }

    # 함수 선택
    # selected_function_name = function_call.name
    
    # answer_response = search_pdf(prompt)
    return response
    
