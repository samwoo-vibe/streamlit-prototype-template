# 삼우 Streamlit 프로토타입 개발 규칙

이 저장소를 수정하는 모든 AI 에이전트와 사람은 아래 규칙을 따라야 한다.

## BMAD 필수 게이트

모든 신규 기능, 수정, 리팩터링, 버그 해결은 코드 작성 전에 BMAD Method를 사용한다.
요청이 작아 보여도 BMAD 단계를 생략하지 않는다.

1. 작업 시작 시 `.agents/skills/bmad-help/SKILL.md`를 읽고 현재 상태에 맞는
   BMAD 워크플로를 결정한다.
2. 신규 프로토타입은 최소한 `bmad-product-brief`를 완료한다. 아이디어가 모호하면
   먼저 `bmad-brainstorming`을 수행한다.
3. 기존 기능의 추가·수정·버그 해결은 최소한 `bmad-quick-dev`를 수행해 구현 가능한
   명세와 인수 조건을 만든다.
4. 선택한 BMAD 스킬의 `SKILL.md`를 완전히 읽고 단계와 사용자 확인 지점을
   순서대로 따른다.
5. BMAD 산출물을 `_bmad-output/`에 저장하고 필수 기획 산출물이 완료된 후에만
   애플리케이션 코드를 작성한다.
6. 구현 후 BMAD 산출물의 요구사항과 인수 조건을 기준으로 결과를 검증한다.

BMAD는 템플릿에 미리 설치되어 있다. 사용자 PC에서 Node.js, npm, npx 또는 BMAD
설치기를 실행하지 않는다. `_bmad/`와 `.agents/skills/`의 공식 BMAD 파일을 임의로
삭제하거나 축약하지 않는다.

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

1. BMAD 필수 게이트를 완료하고 기획 또는 변경 명세를 확정한다.
2. 데이터 입력·출력을 `schemas/`에 정의한다.
3. BMAD 인수 조건에 대응하는 실패 테스트를 먼저 작성한다.
4. 업무 로직을 `services/`에 구현한다.
5. 필요할 때만 모델과 repository를 추가한다.
6. 마지막에 Streamlit 화면을 연결한다.
7. BMAD 산출물과 구현 결과를 대조한다.
8. `uv run pytest`를 실행하고 전체 통과를 확인한다.

## 완료 조건

- `uv sync` 성공
- `uv run pytest` 전체 통과
- `uv run streamlit run app.py` 실행 성공
- `src/` 내부에 `import streamlit`이 없음
- `.env`와 `data/*.db`가 Git 추적 대상이 아님
- 해당 작업의 BMAD 산출물이 `_bmad-output/`에 존재
- BMAD 인수 조건과 테스트 결과가 서로 대응
