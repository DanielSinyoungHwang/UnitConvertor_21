# UnitConvertor_21 — Defect List

**형식:** ISS (이슈) · DEF (결함)  
**갱신:** 세션 종료 시 Report §8과 동기화  
**SSOT:** 요구사항은 [`PRD.md`](./PRD.md) 참조

---

## 상태 범례

| 상태 | 의미 |
|------|------|
| OPEN | 미해결 |
| WONTFIX | 의도적 미수정 (범위 외·선택) |
| CLOSED | 해결 완료 |

---

## 결함 목록

| ID | 유형 | 제목 | 근본 원인 | 상태 | 관련 |
|----|------|------|-----------|------|------|
| DEF-001 | DEF | 레거시 `main()` God Function — 파싱·변환·출력 혼재 | 절차적 단일 스크립트 구조 | CLOSED | Report/03 — domain/app/cli 분리 |
| DEF-002 | DEF | if/elif 단위 분기 — OCP 위반 | 하드코딩 분기 구조 | CLOSED | Report/03 — UnitRegistry + Protocol |
| DEF-003 | DEF | 변환 비율 이중 정의 (코드 + config) | REFACTOR 전 DEFAULT 상수 잔존 | CLOSED | Report/03 — NFR-06 units.json 단일 출처 |
| DEF-004 | DEF | 입력 검증 부재 (음수·형식·미지원 단위) | 레거시에 parser 계층 없음 | CLOSED | Report/03 — input_parser.py |
| DEF-005 | DEF | 테스트 불가 구조 (stdin/print 결합) | I/O와 도메인 미분리 | CLOSED | Report/03 — NFR-05 fixture 기반 테스트 |
| ISS-001 | ISS | YAML config 미지원 | FR-06 JSON만 구현, YAML 파서 미추가 | CLOSED | `config/units.yaml`, `config_loader` PyYAML 지원 |
| ISS-002 | ISS | Mom Test 미실시 | 비개발자 UX 검증 일정 미정 | CLOSED | Report/08 — UX-001~004 개선 제안 기록 |
| ISS-003 | ISS | Report/07 Prompting Transcript 없음 | Export 미실시 | CLOSED | Prompting/07 소급 작성 |
| ISS-004 | ISS | CLI UX 개선 여지 | Unknown unit·등록 형식 혼동·format 목록 미안내 | CLOSED | Report/09 — UX-001~004 구현 |

---

## 추가·갱신 프롬프트

```
defect_list.md에 정리해줘
```

새 결함 발견 시 위 표에 행을 추가하고, 해당 세션 Report §8에도 동일 내용을 기록한다.
