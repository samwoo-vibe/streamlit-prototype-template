# 삼우 Streamlit 프로토타입 개발 규칙

이 저장소를 수정하는 모든 AI 에이전트와 사람은 아래 규칙을 따라야 한다.

## 목적

- Streamlit은 아이디어, 화면, 업무 흐름을 검증하는 프로토타입이다.
- 정식 서비스 전환 시 `services`, `schemas`, `repositories`, `models`를
  FastAPI + PostgreSQL 백엔드에서 최대한 재사용할 수 있어야 한다.
- React 화면은 정식 전환 단계에서 별도로 구현한다.

## 강제 아키텍처

1. `streamlit` import와 `st.*` 호출은 `app.py`와 `pages/`에서만 허용한다.
2. 계산, 검증, 업무 규칙은 `src/samwoo_prototype/services/`에 작성한다.
3. 입력과 출력 구조는 Pydantic 모델로 정의한다.
4. DB 접근은 `repositories/`를 통해서만 수행한다.
5. SQLAlchemy ORM을 사용하고 SQLite 전용 SQL을 작성하지 않는다.
6. 중요한 업무 상태를 `st.session_state`에만 저장하지 않는다.
7. 환경별 설정은 환경변수로 받고 비밀번호나 토큰을 코드에 넣지 않는다.
8. `.env`, DB 파일, 개인정보, 실제 회사 데이터를 Git에 커밋하지 않는다.
9. 스키마를 변경하면 모델과 관련 테스트를 함께 수정한다.
10. 새 업무 로직에는 최소 한 개 이상의 pytest 테스트를 작성한다.

## 금지 사항

- Streamlit 버튼 처리문 안에 SQL, 긴 계산식, 파일 변환 로직 작성
- 화면 모듈에서 SQLAlchemy 세션 직접 사용
- SQLite의 `PRAGMA`, 동적 타입 등 SQLite 전용 동작에 의존
- 절대 경로 사용
- 운영 서버, Coolify, Hermes, 사내 운영 DB에 직접 연결
- 인증 없는 상태로 개인정보나 민감정보를 수집
- 실제 비밀번호, API 키, SSH 키를 생성하거나 저장소에 기록

## 작업 절차

1. 요청을 한 문단으로 다시 정의하고 불명확한 업무 규칙을 확인한다.
2. 데이터 입력·출력을 `schemas/`에 정의한다.
3. 실패하는 테스트를 먼저 작성한다.
4. 업무 로직을 `services/`에 구현한다.
5. 필요할 때만 모델과 repository를 추가한다.
6. 마지막에 Streamlit 화면을 연결한다.
7. `uv run pytest`를 실행하고 전체 통과를 확인한다.

## 완료 조건

- `uv sync` 성공
- `uv run pytest` 전체 통과
- `uv run streamlit run app.py` 실행 성공
- `src/` 내부에 `import streamlit`이 없음
- `.env`와 `data/*.db`가 Git 추적 대상이 아님

