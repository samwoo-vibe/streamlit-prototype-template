# 삼우 Streamlit 프로토타입 템플릿

비개발자가 아이디어와 업무 흐름을 빠르게 검증하기 위한 사내 표준 템플릿입니다.
정식 서비스로 채택되면 업무 로직과 데이터 모델을 재사용해
React + FastAPI + PostgreSQL 서비스로 전환합니다.

AI 코딩 에이전트는 작업을 시작하기 전에 반드시 [`AGENTS.md`](AGENTS.md)를
읽고 모든 규칙을 따라야 합니다.

## 직원 PC 준비

직접 설치할 프로그램은 `uv` 하나입니다. Python 3.13과 모든 Python 패키지는
uv가 프로젝트별로 자동 준비합니다. Node.js, Docker, WSL, FastAPI,
PostgreSQL은 설치하지 않습니다.

## 실행

Windows에서 `start.cmd`를 더블클릭합니다. 최초 실행은 Python과 패키지를
다운로드하므로 시간이 조금 걸릴 수 있습니다.

명령줄에서는 다음과 같이 실행할 수 있습니다.

```powershell
uv sync
uv run streamlit run app.py
```

테스트:

```powershell
uv run pytest
```

## 저장 데이터

개발 데이터는 `data/prototype.db`에 저장됩니다. 이 파일은 Git에 올라가지
않습니다. 중요한 업무 데이터나 개인정보를 프로토타입에 입력하지 마세요.

## 폴더 역할

- `app.py`, `pages/`: Streamlit 화면만 작성
- `src/samwoo_prototype/services/`: 계산과 업무 규칙
- `src/samwoo_prototype/schemas/`: 입력·출력 데이터 구조
- `src/samwoo_prototype/repositories/`: 데이터 조회·저장
- `src/samwoo_prototype/models.py`: SQLAlchemy 테이블 모델
- `tests/`: 화면과 분리된 업무 로직 테스트

