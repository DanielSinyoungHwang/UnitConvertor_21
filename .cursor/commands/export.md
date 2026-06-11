# Export — UnitConvertor_21

세션 종료 시 **작업 보고서**와 **프롬프트 이력**을 아래 경로에 저장한다.

| 산출물 | 경로 | 설명 |
|--------|------|------|
| 작업 보고서 | `Report/NN.md` | 세션 목표·산출물·결정·검증·다음 액션 요약 |
| 프롬프트 이력 | `Prompting/NN.md` | Turn 단위 대화·명령·결과 Transcript Export |

---

## 파일명 규칙

```
Report/NN.md
Prompting/NN.md
```

| 항목 | 규칙 |
|------|------|
| `NN` | 2자리 순번 (`01`, `02`, …). `Report/`·`Prompting/` 각각 기존 최대값 +1 |
| 번호 일치 | 동일 Export 실행에서 Report와 Prompting은 **같은 NN** 사용 |
| 폴더 | 없으면 `Report/`, `Prompting/` 생성 |

**예시**

- `Report/01.md`
- `Prompting/01.md`

---

## 실행 절차

1. **NN 결정** — `Report/`·`Prompting/` 기존 `NN.md` 목록 확인 후 다음 번호 선택
2. **세션 식별** — 주제·단계·상태(완료/진행 중) 확정
3. **Report 작성** — `Report/NN.md` 생성 (아래 템플릿)
4. **Transcript 작성** — 현재 채팅 전체를 Turn 단위로 `Prompting/NN.md`에 기록
5. **완료 보고** — 생성된 파일 경로 2개를 사용자에게 표로 안내

---

## Report 템플릿 (`Report/NN.md`)

```markdown
# UnitConvertor_21 — <주제> 보고서

**작성일:** YYYY-MM-DD
**프로젝트:** UnitConvertor_21
**세션:** <단계>
**상태:** <완료 / 진행 중>

---

## 1. 세션 목표

## 2. 산출물

| 파일 | 설명 |
|------|------|

## 3. 핵심 결정

## 4. 검증 결과

(해당 시 pytest·실행 결과·입력 검증 등)

## 5. AI 활용 회고

- 도움이 된 순간:
- 한계·주의점:

## 6. 다음 액션

- [ ] ...

## 7. 관련 문서

- `Prompting/NN.md`
```

---

## Transcript 템플릿 (`Prompting/NN.md`)

```markdown
# Export Transcript — UnitConvertor_21 <주제>

**Exported:** YYYY-MM-DD
**Session:** <단계>

---

## Turn N — User

> (사용자 메시지 요약 또는 인용)

---

## Turn N — Agent

(에이전트 응답·실행한 명령·결과 요약)

---

## Session State

| 항목 | 값 |
|------|-----|

---

## Prompting Context (재개용)

```
프로젝트: UnitConvertor_21
단계: ...
완료: ...
진행 중: ...
다음: ...
참고: Report/NN.md
```
```

---

## Transcript 작성 규칙

- 현재 세션의 **모든 User/Agent Turn**을 시간순으로 기록
- 사용한 **Cursor Command** (`/export` 등) 명시
- 파일 생성·수정·pytest 실행 등 **실제 수행 결과**만 기재 (추측 금지)
- 민감 정보(API 키·토큰)는 `[REDACTED]` 처리

---

## 체크리스트

- [ ] `Report/NN.md`·`Prompting/NN.md` **동일 NN**
- [ ] Report에 산출물 경로·검증 결과 반영
- [ ] Transcript에 Turn 단위 대화·Session State·재개용 Context 포함
- [ ] **git commit 하지 않음** (사용자 요청 시만)
