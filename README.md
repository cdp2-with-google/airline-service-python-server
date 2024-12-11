# CDP2 - LLM 모델을 이용한 항공사 고객서비스 AI Agent (BE)
## 프로젝트 목적
- 항공사 고객 서비스 팀의 업무 효율성, 고객 만족도를 극대화하기 위한 AI 기반 고객 지원 웹페이지를 개발
- 항공권 예약, 일정 변경, 환불 요청, 비행 정보 조회 등 다양한 고객 문의에 실시간으로 대응할 수 있는 LLM 기반의 자동화된 고객 지원 시스템

## 배경 지식
### 1. AI Agent
- 사용자의 요청에 자동으로 응답하고, 외부 시스템과 상호작용하여 트랜잭션을 처리하는 자율적 프로그램
- 본 프로젝트에서는 LLM(Google Gemini 1.5 pro)를 사용한 응답 생성 및 외부 시스템과 연동을 통해, Google Calendar/Google Maps/Gmail 등 트랜잭션 처리

### 2. RAG(Retrieval Augmented Generation)
- '지식 검색' + '언어 생성'
- 질문에 답하기 위해 필요한 지식을 외부 데이터베이스에서 검색하여 활용
<img width="682" alt="image" src="https://github.com/user-attachments/assets/44270937-7a89-4cec-b7d0-12b81889ff0b">


### 3. ReAct(Reason + Act) Architecture
- LLM을 활용해 응답 생성뿐만 아니라, 외부 정보 관련 처리까지 판단하는 아키텍처
<img width="682" alt="스크린샷 2024-12-11 오후 6 43 48" src="https://github.com/user-attachments/assets/0b4ef317-8fd8-42ef-899c-950227459d0f">


## System Architecture
<img width="764" alt="스크린샷 2024-12-09 오후 9 56 34" src="https://github.com/user-attachments/assets/ae765fb0-573f-48ef-9ed0-f07c035f054f">

## 사용 기술
- LLM model: Gemini 1.5 pro
- Python, Flask, Langchain, Firebase
- Google Cloud Platform: Vertex AI, Cloud run, Agent Builder
- Collaboraiton Tool: Notion, Github

## 핵심 기능
#### 채팅으로 항공사 규정/약관 조회 및 항공편 예약, Calendar 일정 추가까지 One-Stop 처리 서비스
- ReAct 기반 Tool 선택 로직
- Vertex AI Search 활용한 RAG Tool
- 공공데이터 활용 항공편 조회 Tool
- Firestore 항공편 예약 Tool
- Google OAuth 및 Google Calendar 일정 자동 생성
- Google Cloud run - Serverless 배포

### Google OAuth2.0 Login (JWT Token 활용)
<div style="display: flex; justify-content: center; align-items: center;">
<img width="1396" alt="스크린샷 2024-12-10 오후 3 00 56" src="https://github.com/user-attachments/assets/125d0158-1604-43b0-a722-44f7a3e7eed1">

<div style="display: flex; justify-content: center; align-items: center;">
<img width="400" alt="스크린샷 2024-12-11 오후 6 50 05" src="https://github.com/user-attachments/assets/f645a322-b7aa-4e19-9f0f-eb502725f270">
<img width="400" alt="스크린샷 2024-12-11 오후 6 50 27" src="https://github.com/user-attachments/assets/8e847831-e6e1-4412-81ae-c6b5dcc6b275">



## 기대 효과
- CS 효율성 향상: 고객 서비스 팀의 일상적인 반복 업무 자동화 → 고객 응대 시간 단축
- 24/7 실시간 지원: 24시간 실시간 응답으로 고객이 필요한 정보를 언제든지 즉시 제공 
- 글로벌 대응 가능: 다국어 지원이 가능한 LLM을 통해 다양한 언어로 서비스 제공
- 비용 절감: CS 자동화 → 인건비, 전화 상담, 이메일 처리 비용 감소
- 사용자 경험(만족도 및 신뢰도) 향상: 고객의 긴급 요청에도 즉각적이고 정확한 응대 제공
- 데이터 기반 서비스 개선: 고객 문의 데이터 분석을 통한 맞춤형 서비스 제공
