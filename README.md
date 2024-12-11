# LLM 모델을 이용한 항공사 고객서비스 AI Agent (BE) 🛩️
## 🎥 시연 영상
https://www.youtube.com/watch?v=uSKJbtROF4M

## 💡 프로젝트 목적
- 항공사 고객 서비스 팀의 업무 효율성, 고객 만족도를 극대화하기 위한 AI 기반 고객 지원 웹페이지를 개발
- 항공권 예약, 일정 변경, 환불 요청, 비행 정보 조회 등 다양한 고객 문의에 실시간으로 대응할 수 있는 LLM 기반의 자동화된 고객 지원 시스템

## ✅ 배경 지식
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
<img width="682" alt="스크린샷 2024-12-11 오후 7 43 29" src="https://github.com/user-attachments/assets/aef62006-9033-4a45-a84c-9988bc831ca7">


## 🌐 사용 기술
- LLM model: Gemini 1.5 pro
- Python, Flask, Langchain, Firebase
- Google Cloud Platform: Vertex AI, Cloud run, Agent Builder
- Collaboraiton Tool: Notion, Github

## ⭐️ 핵심 기능
### 채팅으로 항공사 규정/약관 조회 및 항공편 예약, Calendar 일정 추가까지 One-Stop 처리 서비스
- ReAct 기반 Tool 선택 로직
- Vertex AI Search 활용한 RAG Tool
- 공공데이터 활용 항공편 조회 Tool
- Firestore 항공편 예약 Tool
- Google OAuth 및 Google Calendar 일정 자동 생성
- Google Cloud run - Serverless 배포
### Agent의 사용자 요청 처리 구조
<img width="833" alt="스크린샷 2024-12-11 오후 10 43 56" src="https://github.com/user-attachments/assets/5f3e3d66-54f4-4d74-b81f-61c2da734860">


## 1. OAuth2.0 Google Login (JWT Token 활용)
### Flow
<img width="550" src="https://github.com/user-attachments/assets/db28358b-279f-4fc7-88f1-1d5b3788c779" alt="20">

<img width="100%" alt="스크린샷 2024-12-10 오후 3 00 56" src="https://github.com/user-attachments/assets/125d0158-1604-43b0-a722-44f7a3e7eed1">

<div style="display: flex; justify-content: center; align-items: center;">
<img width="49.7%" alt="스크린샷 2024-12-11 오후 6 59 45" src="https://github.com/user-attachments/assets/3b65e339-158e-47df-a51b-6cb2662f1e4e">
<img width="49.7%" alt="스크린샷 2024-12-11 오후 6 59 12" src="https://github.com/user-attachments/assets/825f82d6-d59f-4a7f-adb0-38494283f41c">
</div>

## 2. 항공사 규정/약관 관련 문의 처리
- Vertex AI App의 Datastore 문서 파싱, 벡터화 처리 자동화(Layout Parser)
- Data Storage에 저장된 파일 데이터 기반 → 정확하고 신뢰도 높은 답변 생성
<img width="100%" alt="스크린샷 2024-12-10 오후 3 00 45" src="https://github.com/user-attachments/assets/0bceeeb5-ac00-46e9-bf42-feef5467974a">
<div style="display: flex; justify-content: center; align-items: center;">
<img src="https://github.com/user-attachments/assets/5abe05d0-59ae-47e7-bc39-3243ceac8d5f" alt="25" width="49.7%">
<img src="https://github.com/user-attachments/assets/16251401-29d1-4031-b5d6-b8cb3a4660ed" alt="26" width="49.7%">
</div>

## 3. 항공편 조회·예약
- 공공데이터포털 [국제선 항공기 스케줄 데이터 활용](https://www.data.go.kr/data/15003087/fileData.do#tab-layer-file)
- 사용자의 문의 챗에서 '날짜', '출발 공항', '도착 공항' 파라미터를 추출하여 항공편 일정 리스트 조회
- "N번째 항공편으로 예약해줘" 또는 "N시 N분에 출발하는 항공편으로 예약해줘" 등의 채팅으로 항공편 예약 진행
- 현재 항공편 결제 시스템은 시뮬레이션 목적의 Mocking 방식으로 구현 (추후 실제 결제 시스템과의 연동 가능하도록 설계)
<div style="display: flex; justify-content: center; align-items: center;">
<img width="49.7%" alt="스크린샷 2024-12-11 오후 7 36 28" src="https://github.com/user-attachments/assets/f7b06fe2-c8e1-4266-ba7c-988ec8ee8d16">
<img width="49.7%" alt="스크린샷 2024-12-11 오후 7 37 34" src="https://github.com/user-attachments/assets/12354fc5-d3cf-495a-95e8-e46ddec0899c">
</div>
<div style="display: flex; justify-content: center; align-items: center;">
<img width="49.7%" alt="스크린샷 2024-12-11 오후 7 37 57" src="https://github.com/user-attachments/assets/c09894b5-e14c-4be9-bdc1-52be047b0bb7">
<img width="49.7%" alt="스크린샷 2024-12-11 오후 7 38 19" src="https://github.com/user-attachments/assets/c1524bf9-3b36-4505-8ab5-701a399cabd8">
</div>

### 정확한 Tool Selection 위해, Tool별 parameter 구체화 및 Example 강화
<div style="display: flex; justify-content: center; align-items: center;">
<img width="49.7%" alt="스크린샷 2024-12-11 오후 10 50 47" src="https://github.com/user-attachments/assets/58f415fc-002b-4519-acca-17d04d90489f">
<img width="49.7%" alt="스크린샷 2024-12-11 오후 10 51 05" src="https://github.com/user-attachments/assets/14ff9bcf-e0f9-417c-9a8d-d9aa03824cd6">
</div>

## 4. Google Calendar 일정 자동 추가
- Google Calendar API 연동하여 이벤트 자동 생성 처리
- String 타입의 날짜와 시간을 합쳐 한국 시간대(KST)로 변환 및 ISO 8601 포맷팅
  
<div style="display: flex; justify-content: center; align-items: center;">
<img width="49.7%" alt="캘린더1" src="https://github.com/user-attachments/assets/ff000f5b-5cb5-4495-bd8b-96a937ce1796">
<img width="49.7%" alt="캘린더2" src="https://github.com/user-attachments/assets/f0d43b38-3fc1-4e90-ab10-e633bff512b3">
</div>

## 기대 효과
- CS 효율성 향상: 고객 서비스 팀의 일상적인 반복 업무 자동화 → 고객 응대 시간 단축
- 24/7 실시간 지원: 24시간 실시간 응답으로 고객이 필요한 정보를 언제든지 즉시 제공 
- 글로벌 대응 가능: 다국어 지원이 가능한 LLM을 통해 다양한 언어로 서비스 제공
- 비용 절감: CS 자동화 → 인건비, 전화 상담, 이메일 처리 비용 감소
- 사용자 경험(만족도 및 신뢰도) 향상: 고객의 긴급 요청에도 즉각적이고 정확한 응대 제공
- 데이터 기반 서비스 개선: 고객 문의 데이터 분석을 통한 맞춤형 서비스 제공
