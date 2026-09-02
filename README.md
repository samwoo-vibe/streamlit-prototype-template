# 삼우 Streamlit 프로토타입 템플릿

비개발자가 아이디어와 업무 흐름을 빠르게 검증하기 위한 사내 표준 템플릿입니다.
정식 서비스로 채택되면 업무 로직과 데이터 모델을 재사용해
React + FastAPI + PostgreSQL 서비스로 전환합니다.

AI 코딩 에이전트는 작업을 시작하기 전에 반드시 [`AGENTS.md`](AGENTS.md)를
먼저 읽고 모든 규칙을 따라야 합니다. 에이전트용 개발·아키텍처·BMAD·보안·검증
규칙은 README가 아니라 `AGENTS.md`를 기준으로 합니다.

## BMAD 작업 흐름

이 절은 이 템플릿으로 파생 앱을 바이브코딩하는 작업에만 적용됩니다. 회사 Coolify,
프로비저너 운영이나 템플릿 자체의 유지보수 절차를 BMAD로 통제한다는 뜻이 아닙니다.
또한 검토·배포용 인계 ZIP에는 BMAD 도구와 산출물을 의도적으로 넣지 않으므로, 그 ZIP을
푼 private 배포 저장소의 운영 유지보수에도 이 절을 적용하지 않습니다. 바이브코딩은
BMAD가 설치된 원래 작업공간에서 마친 뒤 검증된 소스만 인계합니다.

BMAD 파일은 템플릿에 미리 포함되어 있습니다. `bmad-help`로 현재 상태와 다음
단계를 확인합니다. 신규 프로토타입은 승인된 `bmad-product-brief` 뒤에
`bmad-build`의 plan-code-review 경로로 구현합니다. 기존의 제한된 변경도 구현 전에
`bmad-build` 명세·인수 조건·테스트를 갖춥니다. 개인정보·권한·외부 연동·지속 데이터
모델·다수 화면 또는 역할·정식 서비스 전환·큰 의존성이 핵심인 작업은 PRD부터
Readiness까지의 전체 BMAD 경로를 사용합니다. 시작 전
[`_bmad-output/workflow-status.md`](_bmad-output/workflow-status.md)에서 경로와
구현 허용 상태를 확인하며, 상세 기준은 [`docs/BMAD-WORKFLOW.md`](docs/BMAD-WORKFLOW.md)에
있습니다. 각 워크플로의 질문과 승인 지점에서는 사용자 응답을 기다립니다.

## 직원 PC 준비

직접 설치할 프로그램은 Git과 uv 두 개입니다. Python 3.13과 모든 Python 패키지는
uv가 프로젝트별로 자동 준비합니다. Node.js, Docker, WSL, FastAPI,
PostgreSQL은 설치하지 않습니다.

## 실행

Windows에서 `start.cmd`를 더블클릭합니다. 최초 실행은 Python과 패키지를
다운로드하므로 시간이 조금 걸릴 수 있습니다. `.env`가 없으면 `start.cmd`가
`.env.example`을 복사해 만들어 주며, 로컬에서는 SQLite를 사용합니다.

명령줄에서는 다음과 같이 실행할 수 있습니다.

```powershell
copy .env.example .env
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

바이브코딩 중에는 이 공개 템플릿이나 다른 GitHub 저장소에 직접 push하지 않습니다.
아래 인수인계 ZIP을 Nextcloud에 올리면 관리자가 검토한 뒤 `samwoo-vibe` 조직에 별도
private 앱 저장소를 만들고 승인된 소스를 루트에 풉니다. 그 저장소의 `main` 첫 push가
Coolify 개발 환경을 만들고, 이후 `main` push가 같은 앱을 자동 재배포합니다.

- 공개 서비스: `streamlit:8501`
- 헬스체크: `/_stcore/health`
- 운영 DB: 중앙 PostgreSQL의 앱 전용 database와 role
- 로컬 SQLite 데이터: 배포하지 않음
- 앱 기준 URL: 프로비저너가 주입하는 `APP_BASE_URL`
- 외부 접근: 기본 공개(회사 공용 HTTP Basic Auth 없음)
- 실행 격리: 비특권 사용자, capability 제거, `no-new-privileges`, 512MB·1 CPU·256 PID 제한
- 요청 크기: 파일 업로드와 WebSocket 메시지 각각 최대 50MB

자동 배포 URL은 인터넷에서 접근할 수 있습니다. 개인정보나 업무상 민감정보를 다루기
전에는 이 앱 안에 인증·인가를 직접 구현하고 서버 측에서 권한을 검사해야 합니다.
인증을 구현하기 전에는 실제 민감 데이터를 입력하지 마세요. 예제 메모 저장·조회는 로컬
SQLite 프로토타입에서만 열리고, PostgreSQL을 사용하는 공개 배포에서는 익명 DB 증가와
저장 데이터 노출을 막기 위해 모두 비활성화됩니다.

50MB보다 큰 파일을 처리해야 하면 `.streamlit/config.toml`만 임의로 높이지 말고 실제 최대
동시 작업의 메모리를 측정해 `mem_limit`과 업로드 한도를 함께 조정해야 합니다.

## 저장 데이터

개발 데이터는 `data/prototype.db`에 저장됩니다. 이 파일은 Git에 올라가지
않습니다. 앱 자체 인증·인가를 구현하기 전에는 중요한 업무 데이터나 개인정보를
프로토타입에 입력하지 마세요. 배포본에서 쓰기를 활성화할 때는 인증·인가의 서버 측
검사와 함께 요청 빈도·용량 제한, 중복 요청 방지, 보존·정리 정책을 구현합니다.

## 소스코드 인수인계

Nextcloud 또는 별도 Git 저장소로 개발 결과를 넘길 때는 프로젝트 폴더 전체가 아니라
다음 명령으로 만든 인수인계본을 사용합니다.

```powershell
uv run python scripts/export_handoff.py
```

`_handoff/`에 앱 실행과 향후 React + FastAPI 마이그레이션에 필요한 소스만 담긴
폴더와 ZIP이 생성됩니다. 실행 소스와 함께 테스트·린트 설정·인수인계 스크립트가
포함됩니다. BMAD 파일, 개발 DB, 실제 데이터, 캐시와 Git 이력은 포함되지 않습니다.
