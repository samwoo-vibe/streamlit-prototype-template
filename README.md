# 삼우 Streamlit 프로토타입 템플릿

비개발자가 아이디어와 업무 흐름을 빠르게 검증하기 위한 사내 표준 템플릿입니다.
정식 서비스로 채택되면 업무 로직과 데이터 모델을 재사용해
React + FastAPI + PostgreSQL 서비스로 전환합니다.

AI 코딩 에이전트는 작업을 시작하기 전에 반드시 [`AGENTS.md`](AGENTS.md)를
먼저 읽고 모든 규칙을 따라야 합니다. 에이전트용 개발·아키텍처·BMAD·보안·검증
규칙은 README가 아니라 `AGENTS.md`를 기준으로 합니다.

## BMAD 작업 흐름

BMAD 파일은 템플릿에 미리 포함되어 있습니다. `bmad-help`로 현재 상태와 다음
단계를 확인하고, 신규 프로토타입은 `bmad-product-brief`로 요구사항을 정리한 뒤
구현 단계에서는 `bmad-quick-dev`를 사용합니다. 구현 결과는 필요할 때
`bmad-code-review`로 별도 검토합니다. 각 워크플로의 질문과 승인 지점에서는
사용자 응답을 기다립니다.

## 직원 PC 준비

직접 설치할 프로그램은 Git과 uv 두 개입니다. Python 3.13과 모든 Python 패키지는
uv가 프로젝트별로 자동 준비합니다. Node.js, Docker, WSL, FastAPI,
PostgreSQL은 설치하지 않습니다.

## 실행

Windows에서 `start.cmd`를 더블클릭합니다. 최초 실행은 Python과 패키지를
다운로드하므로 시간이 조금 걸릴 수 있습니다.

명령줄에서는 다음과 같이 실행할 수 있습니다.

```powershell
uv sync
uv run alembic upgrade head
uv run streamlit run app.py
```

테스트:

```powershell
uv run pytest
```

직원 PC에서는 PostgreSQL이나 Docker를 설치하지 않습니다. 로컬 실행은 기본값인
SQLite를 사용하고, `main` 브랜치 배포 시 Coolify가 앱 전용 PostgreSQL과
`DATABASE_URL`을 자동으로 준비합니다. 컨테이너는 시작 전에 Alembic migration을
적용한 다음 Streamlit을 실행합니다.

## 자동 배포

`samwoo-vibe` 조직에서 이 템플릿으로 저장소를 만든 후 `main` 브랜치에 push하면
Coolify 개발 환경에 자동으로 등록·배포됩니다. 이후 `main` push도 자동 재배포됩니다.

- 공개 서비스: `streamlit:8501`
- 헬스체크: `/_stcore/health`
- 운영 DB: 중앙 PostgreSQL의 앱 전용 database와 role
- 로컬 SQLite 데이터: 배포하지 않음
- 외부 접근: Coolify에서 회사 공용 HTTP Basic Auth를 먼저 적용

## 저장 데이터

개발 데이터는 `data/prototype.db`에 저장됩니다. 이 파일은 Git에 올라가지
않습니다. 중요한 업무 데이터나 개인정보를 프로토타입에 입력하지 마세요.

## 소스코드 인수인계

Nextcloud 또는 별도 Git 저장소로 개발 결과를 넘길 때는 프로젝트 폴더 전체가 아니라
다음 명령으로 만든 인수인계본을 사용합니다.

```powershell
uv run python scripts/export_handoff.py
```

`_handoff/`에 앱 실행과 향후 React + FastAPI 마이그레이션에 필요한 소스만 담긴
폴더와 ZIP이 생성됩니다. BMAD 파일, 테스트, 개발 DB, 실제 데이터, 캐시와 Git 이력은
포함되지 않습니다.
