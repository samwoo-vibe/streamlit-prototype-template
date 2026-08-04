# 프로젝트 문서

이 폴더는 BMAD가 프로젝트의 기술·업무 맥락을 확인할 때 사용하는
`project_knowledge` 경로입니다.

## BMAD 작업 흐름

- `bmad-help`: 현재 상태를 확인하고 다음 작업을 안내합니다.
- `bmad-product-brief`: 신규 프로토타입의 목적과 범위를 정리합니다.
- `bmad-quick-dev`: 기능 추가, 수정, 리팩터링과 버그 해결을 구현합니다.
- `bmad-code-review`: 구현 결과를 별도 컨텍스트에서 검토합니다.

작업 규칙과 사용자 승인 지점은 저장소 루트의 [`AGENTS.md`](../AGENTS.md)를
기준으로 합니다. 이 문서는 템플릿의 공통 안내이며, 실제 프로젝트의 Product
Brief와 확정된 요구사항이 생기면 프로젝트에 맞는 문서로 보완합니다.

## 공통 기술 기준

- 로컬 실행과 테스트는 `uv`를 사용합니다.
- 화면은 Streamlit의 `app.py`와 `pages/`에 둡니다.
- 업무 규칙은 `src/samwoo_prototype/services/`에 둡니다.
- 데이터 구조는 `schemas/`, 데이터베이스 접근은 `repositories/`에 둡니다.
- ORM은 SQLAlchemy를 사용하고, 로컬 데이터베이스는 SQLite를 사용합니다.
- 비밀번호, 토큰, 개인정보와 실제 회사 데이터는 문서와 Git에 기록하지 않습니다.

BMAD 산출물은 이 폴더가 아니라 `_bmad-output/`에 저장합니다.
