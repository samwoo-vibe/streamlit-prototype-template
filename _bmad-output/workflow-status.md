# BMAD 작업 상태

이 파일은 복제 직후의 빈 초기 상태다. 코드 변경을 시작하기 전에 경로를 선택하고,
산출물·사용자 승인·구현 허용 상태를 갱신한다. 실제 프로젝트의 상세 기획 내용이나
민감정보는 기록하지 않는다.

```yaml
work_id: template-initial-state
scope: 복제 후 첫 작업의 경로를 선택한다
baseline: null
path: undecided # lightweight | full | undecided
status: not-started # not-started | in-progress | blocked | complete
implementation: blocked # blocked | allowed
artifacts: [] # 상대 경로와 완료 여부
approval:
  user: pending # pending | approved
  next_checkpoint: path-selection
```

새 작업은 `work_id`, `scope`, `baseline`을 바꾸고 `status: in-progress`,
`implementation: blocked`, `approval.user: pending`으로 시작한다. 이전 작업의
`implementation: allowed`나 승인을 재사용하지 않는다.

경량 경로는 `bmad-build` 명세·인수 조건·테스트와 사용자 승인을, 전체 경로는 PRD,
UX(해당 시), Architecture, Epics/Stories, Readiness와 사용자 승인을 완료한 뒤에만
`implementation: allowed`로 변경한다. 경계 작업은 `status: blocked`로 기록하고
사용자에게 경로를 확인한다.
