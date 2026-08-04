---
title: '최신 BMAD 내장본 갱신 및 라이선스 고지'
type: 'chore'
created: '2026-08-04'
status: 'done'
baseline_commit: '439471bf79a2c543f553996a365818d7be8a8c7a'
review_loop_iteration: 0
context:
  - 'AGENTS.md'
  - '_bmad/config.toml'
  - '_bmad/custom/config.toml'
  - '_bmad/custom/bmad-build.toml'
  - 'README.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** 템플릿에 포함된 BMAD 스냅샷이 upstream 최신 main의 구조와 달라 `bmad-build`, `bmad-project-context` 등 최신 기능이 빠져 있고, 공개 배포용 BMAD 라이선스 고지가 없다.

**Approach:** upstream `bmad-code-org/BMAD-METHOD`의 최신 main 스냅샷을 `_bmad/`와 `.agents/skills/`에 반영한다. 삼우 템플릿의 사용자 언어·출력 경로·사용자 참여 규칙과 기존 커스터마이징은 보존하고, 최신 호환성에 필요한 `bmad-quick-dev` 커스터마이징을 `bmad-build` 이름으로 이전한다. README와 AI 도구 연동 범위는 변경하지 않는다.

## Boundaries & Constraints

**Always:** upstream 파일은 임의로 축약하지 않는다. `_bmad-output/`와 앱 소스는 변경하지 않는다. `README.md`, `AGENTS.md`, 앱 코드와 테스트는 변경하지 않는다. 사용자 PC에 Node.js, npm, npx 또는 BMAD 설치기를 요구하지 않는다.

**Ask First:** upstream 최신 main과 최신 stable release가 다를 경우 main 스냅샷을 선택한 현재 요청을 유지할지 추가 확인한다. 기존 커스터마이징의 의미가 최신 스킬과 충돌하면 해당 파일을 삭제하거나 규칙을 완화하지 않고 HALT한다.

**Never:** BMAD 파일을 수작업으로 요약하거나 일부만 남기지 않는다. 원본 템플릿 remote에 push하지 않는다. 기존 `_bmad/custom/` 사용자 규칙을 승인 없이 삭제하지 않는다.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| HAPPY_PATH | upstream 최신 스냅샷과 깨끗한 작업 트리 | 최신 BMAD 스킬·카탈로그·설정·manifest와 라이선스 고지가 반영됨 | 검증 명령 통과 |
| CUSTOMIZATION_COMPATIBILITY | 기존 `bmad-quick-dev.toml` 존재 | `bmad-build.toml`로 의미를 보존해 이전하고 legacy 충돌을 방지함 | 충돌 시 사용자 확인 후 중지 |
| README_PRESERVATION | 변경 전후 README | 파일 내용이 동일함 | 차이가 있으면 중지 |

</frozen-after-approval>

## Code Map

- `_bmad/` -- BMAD 중앙 설정, 모듈 카탈로그, manifest와 실행 스크립트
- `.agents/skills/` -- AI 코딩 도구가 읽는 BMAD 스킬 파일
- `_bmad/custom/` -- 삼우 템플릿의 언어·워크플로 커스터마이징
- `THIRD_PARTY_NOTICES.md` -- BMAD upstream 저작권·MIT 라이선스 고지
- `README.md` -- 보존해야 하는 사용자 안내 문서

## Tasks & Acceptance

**Execution:**

- [x] `_bmad/` -- upstream 최신 main의 core/bmm 설치 산출물로 갱신하고 삼우 설정·경로를 보존한다.
- [x] `.agents/skills/` -- upstream 최신 core/bmm 스킬을 반영하되 v6 호환 shim을 포함한다.
- [x] `_bmad/custom/bmad-build.toml` -- 기존 quick-dev 커스터마이징을 최신 Build 진입점에 맞게 이전한다.
- [x] `_bmad/custom/bmad-quick-dev.toml` -- migration 후 중복·충돌을 제거한다.
- [x] `THIRD_PARTY_NOTICES.md` -- BMAD upstream URL, revision, 저작권자와 MIT License 전문을 기록한다.

**Acceptance Criteria:**

- Given 최신 upstream 스냅샷, when 설치 파일을 비교하면, then `bmad-build`, `bmad-build-auto`, `bmad-project-context`와 최신 help catalog가 존재한다.
- Given 템플릿의 현재 설정, when BMAD 설정 해석기를 실행하면, then Korean communication/document language와 기존 planning/implementation/docs 경로가 유지된다.
- Given 기존 quick-dev 커스터마이징, when `bmad-quick-dev` 호환 shim이 실행되면, then 사용자 확인을 요구하는 legacy rename 상태 없이 `bmad-build`로 전달된다.
- Given 변경 전후 README, when SHA-256을 비교하면, then 해시가 동일하다.
- Given 공개 템플릿, when 라이선스 고지를 확인하면, then BMAD MIT License 전문과 upstream attribution이 존재한다.

## Verification

**Commands:**

- `uv run pytest` -- 기존 전체 테스트 통과
- `uv run python _bmad/scripts/resolve_config.py --project-root .` -- 설정 JSON 출력 성공
- `uv run python _bmad/scripts/resolve_customization.py --skill .agents/skills/bmad-build --key workflow` -- 최신 Build 커스터마이징 해석 성공
- `git diff -- README.md` -- 변경 없음
- `git status --short` -- 의도한 BMAD·라이선스 파일만 변경

## Suggested Review Order

**Build entrypoint**

- 최신 구현 진입점이 전체 Build 워크플로를 정의한다.
  [`SKILL.md:2`](../../.agents/skills/bmad-build/SKILL.md#L2)

- upstream 설치 원본에도 동일한 Build 스킬이 포함된다.
  [`SKILL.md:2`](../../_bmad/bmm/ship/bmad-build/SKILL.md#L2)

**Compatibility and customization**

- 기존 quick-dev 호출은 사용자 입력을 보존한 채 새 Build로 전달한다.
  [`SKILL.md:2`](../../.agents/skills/bmad-quick-dev/SKILL.md#L2)

- 기존 한국어 게이트와 승인 규칙을 새 Build 진입점에 유지한다.
  [`bmad-build.toml:1`](../../_bmad/custom/bmad-build.toml#L1)

**Discovery and installation metadata**

- 설치 revision과 포함 모듈 버전을 고정해 snapshot 출처를 추적한다.
  [`manifest.yaml:1`](../../_bmad/_config/manifest.yaml#L1)

- 최신 Project Context와 Build 명령을 help catalog에 노출한다.
  [`bmad-help.csv:3`](../../_bmad/_config/bmad-help.csv#L3)

- Build, Build Auto, Project Context 스킬 경로를 manifest에 등록한다.
  [`skill-manifest.csv:28`](../../_bmad/_config/skill-manifest.csv#L28)

**Third-party licensing**

- 번들된 BMAD snapshot의 upstream attribution과 MIT License를 고지한다.
  [`THIRD_PARTY_NOTICES.md:1`](../../THIRD_PARTY_NOTICES.md#L1)
