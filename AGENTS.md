# 삼우 Streamlit 프로토타입 개발 규칙

이 저장소를 수정하는 모든 AI 에이전트와 사람은 아래 규칙을 따라야 한다.
README는 사람을 위한 프로젝트 소개와 실행 안내다. 작업 규칙은 이 문서를 단일
기준으로 삼으며, 작업을 시작할 때 이 문서를 끝까지 먼저 읽는다.

## 개발 환경

- 직원 PC에는 Git과 uv만 요구한다.
- Python과 패키지는 uv로 준비한다.
- 직원 PC에 Node.js, npm, npx, Docker, WSL, FastAPI 서버 또는 PostgreSQL 서버를
  설치하도록 안내하지 않는다.
- 로컬 데이터베이스는 SQLite `data/prototype.db`, Coolify 배포 데이터베이스는
  자동 생성된 앱 전용 PostgreSQL이다.
- 로컬 SQLite 데이터는 배포하거나 운영 PostgreSQL로 이전하지 않는다.
- `psycopg[binary]` 의존성은 PostgreSQL 서버 설치를 의미하지 않는다.

## BMAD 필수 게이트

이 게이트의 범위는 이 템플릿에서 파생된 개별 앱의 바이브코딩 작업뿐이다. 회사
Coolify·프로비저너 운영 또는 원본 템플릿 자체의 유지보수 절차에는 적용하지 않는다.
검토·배포용 인계 ZIP에는 BMAD 도구·산출물이 의도적으로 제외되므로, ZIP을 푼 private
배포 저장소의 운영 유지보수에도 적용하지 않는다. BMAD 없는 인계 저장소에서 이 절을
이유로 도구 설치를 요구하거나 작업을 중단하지 않는다.

모든 신규 기능, 수정, 리팩터링, 버그 해결은 코드 작성 전에 BMAD Method를 사용한다.
요청이 작아 보여도 이 게이트를 생략하지 않는다. 작업 시작 시 먼저
[`_bmad-output/workflow-status.md`](_bmad-output/workflow-status.md)를 읽고
`bmad-help`로 현재 상태에 맞는 경로를 확인한다. 새 작업은 이전 작업의 승인이나
`implementation: allowed`를 재사용하지 않고 상태 파일을 다시 초기화한다.

1. 작업 범위가 단일 화면 또는 업무 규칙의 제한된 변경이면 **경량 경로**를 사용한다.
   신규 프로토타입은 승인된 `bmad-product-brief` 뒤에, 기존 변경은 구현 전에
   `bmad-build`로 명세와 인수 조건을 만든다. `bmad-build`의 plan-code-review 경로와
   사용자 승인 지점을 순서대로 따른 뒤 명세·인수 조건·테스트가 갖춰진 경우에만 구현한다.
2. 개인정보·권한·외부 API·지속 데이터 모델·다수 역할/화면·정식 서비스 전환·큰 기능
   의존성 중 하나가 작업의 핵심이면 **전체 BMAD 경로**로 승격한다. `bmad-prd` →
   `bmad-ux`(해당 시) → `bmad-architecture` → `bmad-create-epics-and-stories` →
   `bmad-check-implementation-readiness` 순서로 필요한 산출물을 완료한 뒤,
   `bmad-build`로 구현·검토·사용자 승인 흐름을 진행한다. 신규 프로토타입은 이 순서 전에
   승인된 Product Brief를 갖춰야 한다.
3. 영향 범위가 경량과 승격 사이에서 불명확하면 상태 파일에 `blocked`를 기록하고
   사용자에게 경량 또는 승격 경로를 확인한다. 추정으로 경량 경로를 선택하지 않는다.
4. 선택한 BMAD 스킬의 `SKILL.md`를 완전히 읽고 단계와 사용자 확인 지점을
   순서대로 따른다. 전체 경로는 Readiness가 완료되고 상태 파일이 `implementation:
   allowed`가 되기 전에는 코드를 작성하지 않는다.
5. BMAD 산출물은 `_bmad-output/`에 저장하되, 공개 템플릿에는 빈 초기 상태만
   추적한다. 실제 프로젝트의 상세 기획 산출물이나 민감정보를 이 템플릿에 기록하지 않는다.
6. 구현 후 선택한 경로의 명세·인수 조건과 테스트를 기준으로 결과를 검증한다.

경로 선택, 산출물 위치 및 상태 형식은 [`docs/BMAD-WORKFLOW.md`](docs/BMAD-WORKFLOW.md)를
기준으로 한다. 상태 파일은 CI 차단기가 아니라 에이전트의 작업 게이트다.

BMAD는 템플릿에 미리 설치되어 있다. 사용자 PC에서 Node.js, npm, npx 또는 BMAD
설치기를 실행하지 않는다. `_bmad/`와 `.agents/skills/`의 공식 BMAD 파일을 임의로
삭제하거나 축약하지 않는다.

### BMAD 사용자 참여 원칙

사람이 에이전트와 대화 중인 세션은 BMAD가 다른 스킬이나 상위 워크플로에서 호출되어도
**항상 interactive 실행**으로 취급한다. 스킬 간 호출만으로 headless 실행으로 판정하지
않는다. headless는 사용자 메시지 스트림이 없는 자동화 작업임이 명확할 때만 사용한다.

- 제품 목적, 대상 사용자, 업무 흐름, 입력·출력, 성공 기준과 우선순위에 관한 BMAD
  질문은 실제 사용자에게 직접 한다.
- 에이전트가 사용자 역할을 맡거나 질문에 자문자답하지 않는다. 추론이나 가정을 실제
  사용자 답변처럼 기록하지 않는다.
- 선택한 BMAD 스킬에 `WAIT`, `HALT`, 사용자 확인, 선택 또는 승인 지점이 있으면
  반드시 멈추고 실제 사용자 응답을 기다린다.
- 저장소와 문서에서 확인 가능한 사실은 먼저 조사하되, 확인할 수 없는 제품 의도나 업무상
  판단은 사용자에게 묻는다.
- 사용자가 명시적으로 자율 결정을 요청한 범위에서만 가정을 허용한다. 허용된 가정도
  산출물에 표시하며, 보안·개인정보·데이터 손실·외부 배포처럼 되돌리기 어려운 결정은
  별도로 확인한다.
- 필요한 사용자 답변을 받기 전에는 BMAD 산출물을 완료 상태로 표시하거나 구현으로
  넘어가지 않는다.

### 신규 프로젝트 필수 체크포인트

신규 프로토타입은 `bmad-product-brief`의 **Coaching path**로 시작한다. Fast path,
headless, one-shot 경로를 사용하지 않는다. 사용자가 한 번에 상세 요구사항을 줬더라도
다음 결정을 에이전트가 대신 내리지 않는다.

1. 제품 목적·대상 사용자·현재 문제를 확인하고 사용자 답변을 기다린다.
2. 핵심 업무 흐름·입력·출력·예외 상황을 확인하고 사용자 답변을 기다린다.
3. 범위·우선순위·성공 기준을 확인하고 Product Brief 승인을 기다린다.
4. `bmad-build`의 구현 가능한 명세와 인수 조건을 제시하고 승인을 기다린다.
5. 주요 화면과 핵심 업무 흐름의 동작 가능한 초안을 보여주고 피드백을 기다린다.
6. 테스트 결과와 변경사항을 제시하고 commit·push·배포 승인을 기다린다.

각 지점에서는 명시적으로 `HALT`한다. 질문을 한꺼번에 형식적으로 나열한 뒤 답이 없는
부분을 추론으로 채우지 않는다. 사용자가 “알아서 해”, “묻지 말고 진행”처럼 해당 작업의
자율 진행을 명시적으로 요청한 범위에서만 체크포인트를 줄일 수 있다.

자동 배포된 신규 앱은 기본 공개이며 Coolify의 회사 공용 HTTP Basic Auth를 거치지 않는다.
개인정보나 업무상 민감정보가 필요하면 앱 안에 자체 인증·인가를 구현하고 서버 또는 API에서
권한을 검사한다. 인증 구현 전에는 실제 민감 데이터를 수집하거나 입력하지 않는다. 기본
메모 저장 예제처럼 인증 없는 DB 쓰기·조회는 로컬 SQLite 프로토타입에서만 허용한다.
공개 배포에서 조회나 쓰기를 활성화하려면 서버 측 권한 검사를 먼저 구현하고, 쓰기에는
요청 빈도·용량 제한, 중복 요청 방지, 보존·정리 정책도 함께 구현한다.

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

### 폴더 역할

- `app.py`, `pages/`: Streamlit 화면
- `src/samwoo_prototype/services/`: 계산과 업무 규칙
- `src/samwoo_prototype/schemas/`: 입력·출력 데이터 구조
- `src/samwoo_prototype/repositories/`: 데이터 조회·저장
- `src/samwoo_prototype/models.py`: SQLAlchemy 테이블 모델
- `tests/`: 화면과 분리된 업무 로직 테스트
- `_bmad/`, `.agents/skills/`: 템플릿에 포함된 BMAD Method
- `_bmad-output/`: 기획·구현 산출물

## 사내 배포 규약

배포 규약 전문은 사내 문서 **`마이그레이션 규칙.md`** 에 있다(관리자 보관). 이 템플릿은
그 규약을 이미 만족한 상태로 배포된다. 아래는 **깨뜨리면 배포가 실패하거나 조용히
잘못 동작하는 항목**이므로 임의로 바꾸지 않는다.

- `samwoo-service.yaml`의 `public_service: streamlit` / `public_port: 8501` 조합은
  프로비저너 허용 목록에 등록된 값이다. 바꾸면 배포가 거부된다. 매니페스트가 잘못되면
  GitHub에는 성공으로 보이고 배포만 조용히 안 되므로, push 후 도메인을 눈으로 확인한다.
- 컨테이너가 노출하는 포트는 정확히 하나여야 한다(`EXPOSE 8501`). 관리·메트릭 포트를
  추가로 열면 Traefik이 대상 포트를 정하지 못해 라우팅이 통째로 실패한다.
- `compose.yaml`에 `ports:`를 쓰지 않는다(`expose:`만). 자체 `db:` 서비스를 추가하지
  않는다 - DB는 프로비저너가 중앙 PostgreSQL에 만들어 주고 `DATABASE_URL`로 주입한다.
- `container_name`을 지정하지 않는다. 무중단 교체 배포가 깨진다.
- 명시적 비특권 `user`, `cap_drop: [ALL]`, `no-new-privileges`와 서비스별
  메모리·CPU·PID 제한을 유지한다. 삭제하면 자동 배포 gate에서 거부된다.
- Dockerfile의 공식 base image와 외부 `COPY --from` 이미지는 태그와 OCI digest를 함께
  고정한다. digest를 지우거나 임의 이미지로 바꾸면 동일 커밋 재빌드가 달라질 수 있고
  자동 배포 gate에서 거부된다.
- `traefik.docker.network` 라벨과 required UUID 식을 지우거나 fallback으로 바꾸지
  않는다(R3-3). 프로비저너는 Coolify native Compose 시작 경로를 보장하고 그 경로가
  `COOLIFY_RESOURCE_UUID`를 제공한다. 값이 없으면 잘못된 네트워크로 배포하지 않고
  Compose 해석 단계에서 실패해야 한다.
- 설정이 없을 때 조용히 다른 저장소로 넘어가는 코드를 만들지 않는다(R4-4).
  `DATABASE_URL`은 값이 없으면 즉시 실패해야 한다.
- 시간은 시간대 인식 타입으로 저장하고 표시할 때만 변환한다(R9-1).
- 앱의 기준 URL은 프로비저너가 모든 서비스에 주입하는 `APP_BASE_URL`을 사용한다.
  공개 서비스에만 생길 수 있는 `COOLIFY_URL`이나 하드코딩한 도메인에 의존하지 않는다.
- 스키마 변경은 Alembic revision으로만 수행한다. 앱 시작 코드에서 `create_all()`로
  migration 이력을 우회하지 않는다.
- `.streamlit/config.toml`의 50MB upload/WebSocket 한도를 유지한다. 더 큰 파일이 필요하면
  실제 동시 작업 memory peak를 측정하고 `mem_limit`과 함께 조정한다.
- 공개 배포에서는 `.streamlit/config.toml`의 `client.showErrorDetails = "none"`을 유지해
  예외 메시지·traceback을 브라우저에 노출하지 않는다. 로컬 `start.cmd`만 이를 개발용으로
  덮어쓴다.
- 브라우저에 노출될 값이 아니면 `NEXT_PUBLIC_`/`VITE_` 같은 공개 접두어를 붙이지 않는다.
- 앱 볼륨은 자동 백업 대상이 아니다. 소실되면 안 되는 파일은 관리자에게 백업 등록을
  신청한다.
- PostgreSQL role의 20 connection 제한과 rolling 배포 여유를 위해 DB pool의
  `pool_size=5`, `max_overflow=3`, `pool_timeout=5`를 유지한다. replica나 worker 수를
  늘릴 때는 전체 동시 연결 수를 먼저 계산한다.

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

## 프로젝트 README

- Product Brief에서 프로젝트 이름과 목적이 확정되면 템플릿 `README.md`를 실제
  프로젝트 README로 교체한다.
- 최종 README는 현재 프로젝트의 이름, 목적, 주요 기능과 사용자 실행 방법을
  설명해야 한다.
- 템플릿 자체를 소개하는 문구와 현재 프로젝트에 불필요한 범용 배포·인수인계 설명을
  그대로 남기지 않는다.
- AI 코딩 에이전트가 작업 전에 `AGENTS.md`를 반드시 읽어야 한다는 안내는 유지한다.
- 개인정보나 중요한 운영 데이터를 입력하지 말라는 사용자 주의사항처럼 실제
  프로젝트에도 적용되는 안전 안내는 유지한다.

## Git 및 자동 배포

- 원본 템플릿 저장소 `samwoo-vibe/streamlit-prototype-template`에는 commit하거나
  push하지 않는다.
- 배포 대상 remote는 `samwoo-vibe` 조직에 만든 별도 앱 저장소여야 한다.
- 테스트 결과와 변경사항을 사용자에게 보여주고 명시적 승인을 받은 뒤에만 앱
  저장소의 `main` 브랜치에 commit·push한다.
- push 전에 `Dockerfile`, `compose.yaml`, `samwoo-service.yaml`, `alembic.ini`,
  `migrations/`, `uv.lock`이 유지되는지 확인한다.
- 앱 저장소의 첫 `main` push는 Coolify 개발 환경을 자동 생성·배포하고 이후
  `main` push는 같은 앱을 자동 재배포한다.
- 자동 프로비저너가 앱 전용 PostgreSQL database·role, `DATABASE_URL`, `APP_ENV=dev`,
  `APP_BASE_URL`과 HTTPS 도메인을 준비한다. 신규 앱은 기본 공개이고 공용 HTTP Basic
  Auth는 적용되지 않는다. 접근 제어가 필요하면 앱 안에서 구현한다.
- `APP_ENV`는 운영에서도 항상 `dev`다. 이 값으로 환경을 분기하지 않는다(배포 규약 R5-1).
- 그 외 시크릿(서명 키, 외부 API 키)은 사람이 Coolify 화면에 넣어야 하므로 첫 배포가
  한 번 실패하는 것이 정상이다(배포 규약 R5-6).
- `_handoff/` 산출물은 검토·전환용이며 Coolify 배포에 사용하지 않는다.
- 에이전트는 운영 PostgreSQL, Coolify API, 서버 설정을 직접 조작하거나 자동 배포를
  우회하지 않는다. 실패 시 로그와 manifest를 진단하고 파괴적 조치는 관리자 승인
  없이 수행하지 않는다.

## 소스코드 인수인계

사용자가 Nextcloud 또는 Git 저장소에 결과물을 올려 달라고 하면 현재 작업 폴더 전체를
업로드하지 않는다. 먼저 다음 명령으로 인수인계 전용 산출물을 만든다.

```bash
uv run python scripts/export_handoff.py --project-name 프로젝트명
```

`_handoff/<프로젝트명>-source.zip`만 인수인계 대상으로 사용한다. ZIP 내부에는
프로젝트 파일이 최상위에 바로 들어가며 `<프로젝트명>-source/` 래퍼 폴더는 만들지
않는다. 관리자는 ZIP을 새 private GitHub 저장소의 루트에 압축 해제한 뒤 파일을
이동하거나 추가하지 않고 `main`에 최초 Push할 수 있어야 한다.

- Nextcloud에는 ZIP 파일만 올린다.
- Git에는 ZIP을 새 저장소 루트에 푼 내용만 커밋한다. 현재 작업 저장소의 Git
  이력이나 remote를 재사용하지 않는다.
- 업로드 전에 생성된 `SOURCE-HANDOFF.md`와 파일 목록을 확인한다.
- `.env`, 비밀번호, 토큰, 실제 회사 데이터, 개인정보가 없는지 다시 검사한다.
- `_bmad`, `.agents`, `_bmad-output`, `data`, DB 파일, 캐시, 가상환경, 로그, 임시 파일,
  로컬 업로드 파일 및 기존 `.git`은 절대 포함하지 않는다. 검토 재현에 필요한 `tests/`,
  pytest·Ruff 설정과 `scripts/export_handoff.py`는 포함한다.
- 사용자가 데이터나 BMAD 문서까지 명시적으로 요청해도 소스코드와 같은 묶음에 넣지
  않는다. 필요성과 민감정보를 확인한 뒤 별도 파일로 분리한다.
- ZIP에는 Streamlit 실행에 필요한 `Dockerfile`, `compose.yaml`,
  `samwoo-service.yaml`, `alembic.ini`, `migrations/`, `uv.lock`도 포함되어야 한다.
  따라서 관리자 검토 후 새 private 저장소의 `main`에 최초 Push하면 기존
  GitHub → Provisioner → Coolify 자동 배포 흐름을 시작할 수 있다.

## Git 및 공개 템플릿 규칙

- 이 공개 템플릿은 읽기·복제용으로만 사용한다. 원본 템플릿이나 사용자의 GitHub
  저장소에 바이브코딩 에이전트가 직접 push하지 않는다.
- 신규 앱 GitHub 저장소 URL은 작업 시작 조건이 아니다.
- 사용자가 `_handoff/`의 ZIP을 확인한 뒤 Nextcloud의
  `공유 자료/VibeCoding/<프로젝트명>/`에 자기 계정으로 직접 업로드한다.
- 관리자가 검토 후 별도 private 저장소를 만들고 승인된 소스만 push하면 기존
  GitHub → Provisioner → Coolify 자동 배포가 시작된다.

## 완료 조건

- `uv sync` 성공
- `uv run pytest` 전체 통과
- `uv run streamlit run app.py` 실행 성공
- `src/` 내부에 `import streamlit`이 없음
- `.env`와 `data/*.db`가 Git 추적 대상이 아님
- BMAD가 설치된 원래 바이브코딩 작업공간에서는 해당 산출물과
  `_bmad-output/workflow-status.md`의 경로·승인 상태가 일치
- 같은 원래 작업공간에서는 BMAD 인수 조건과 테스트 결과가 서로 대응
- `README.md`가 템플릿 설명이 아니라 현재 프로젝트를 설명함
- Git remote가 원본 템플릿이 아닌 별도 앱 저장소를 가리킴
- 배포 작업이면 사용자 승인 후 `main` push 성공을 확인함
- `uv run python scripts/export_handoff.py --project-name 프로젝트명` 성공
- 인계 ZIP을 새 저장소 루트에 풀었을 때 `compose.yaml`과
  `samwoo-service.yaml`이 최상위에 존재함
