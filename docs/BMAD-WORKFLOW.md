# 경량 BMAD 작업 게이트

모든 코드 변경은 시작 전에 `_bmad-output/workflow-status.md`를 읽고 `bmad-help`로
경로를 확인한 뒤 상태를 기록한다. 이 상태 파일은 CI 차단기가 아니라 에이전트 작업
게이트다. 경로가 선택되지 않았거나 `implementation`이 `blocked`이면 코드를 작성하지
않는다. 새 작업은 이전 작업의 승인이나 `implementation: allowed`를 재사용하지 않는다.

## 경로 선택

| 작업 특성 | 선택 경로 | 구현 전 조건 |
| --- | --- | --- |
| 단일 화면 또는 업무 규칙의 제한된 변경 | 경량 | `bmad-build` 명세, 인수 조건, 사용자 승인, 테스트 계획 |
| 개인정보, 권한, 외부 API, 지속 데이터 모델, 다수 역할/화면, 정식 서비스 전환 또는 큰 기능 의존성이 핵심 | 전체 BMAD | PRD, UX(해당 시), Architecture, Epics/Stories, Readiness, 사용자 승인 |
| 영향 범위가 불명확 | 차단 | 상태를 `blocked`로 기록하고 사용자에게 경로 확인 요청 |

신규 프로토타입은 먼저 `bmad-product-brief`를 승인받는다. 제한된 구현은 그 뒤
`bmad-build`의 plan-code-review 경로를 사용한다. 기존 변경도 구현 전에
`bmad-build`로 명세와 인수 조건을 만든다.

전체 BMAD 경로는 `bmad-prd` → `bmad-ux`(해당 시) → `bmad-architecture` →
`bmad-create-epics-and-stories` → `bmad-check-implementation-readiness` 순서다.
Readiness가 완료되고 상태 파일에 `implementation: allowed`가 기록되기 전에는
구현하지 않는다. 허용된 뒤에는 `bmad-build`로 구현·검토·사용자 승인 흐름을 진행한다.

## 산출물과 상태 규칙

작업별 산출물은 `_bmad-output/` 아래에 저장하고, 상태 파일에는 민감정보나 실제
프로젝트의 상세 기획 내용을 쓰지 않는다. 공개 템플릿은 복제 직후의 빈 초기 상태만
추적한다. 인수인계 ZIP에는 기존 규칙대로 `_bmad-output/`을 포함하지 않는다.

상태 파일은 다음 항목을 갱신한다.

- `work_id`: 이번 작업을 식별하는 짧은 이름
- `scope`: 변경 목적과 영향 범위를 한 문장으로 요약
- `baseline`: 작업 시작 시의 Git commit
- `path`: `lightweight`, `full`, 또는 `undecided`
- `status`: `not-started`, `in-progress`, `blocked`, 또는 `complete`
- `implementation`: `blocked` 또는 `allowed`
- `artifacts`: 생성한 산출물의 상대 경로와 완료 여부
- `approval`: 사용자 승인 여부와 다음 확인 지점

새 작업을 시작할 때는 `work_id`, `scope`, `baseline`을 바꾸고 `status: in-progress`,
`implementation: blocked`, `approval.user: pending`으로 되돌린다. `complete`는 구현과
검증 결과를 기록한 뒤에만 사용하며, 다음 작업은 반드시 새 상태로 시작한다.

경량 경로는 `bmad-build` 명세·인수 조건·테스트와 명시적 사용자 승인이 있어야
`implementation: allowed`로 바꾼다. 전체 경로는 필수 산출물과 Readiness 완료,
그리고 명시적 사용자 승인까지 모두 있어야 바꾼다. 구현 후에는 산출물의 인수 조건과
테스트 결과를 대조하고 상태를 갱신한다.
