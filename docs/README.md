# UnitConvertor_21 — AI 기반 문서화 가이드

**AI-based Documentation — 3 Principles · Auto Generation · 8 Sections**

이 폴더는 프로젝트 문서의 **단일 진입점**이다. 요구사항·결함·테스트 케이스·보고서 생성 규칙을 한곳에서 관리한다.

---

## 1. 3원칙 (3 Principles)

| # | 원칙 | 설명 |
|---|------|------|
| ① | **SSOT (Single Source of Truth)** | 요구사항은 **한 곳**에만 둔다 → [`PRD.md`](./PRD.md) |
| ② | **Session = Storage Unit** | ARRR(분석·RED·GREEN·REFACTOR) 사이클마다 `Report` + `Prompting` Transcript를 저장한다 |
| ③ | **Number Consistency** | 번호를 문서 종류 간 일치시킨다. 예: `Report/01` ↔ `Prompting/01` ↔ `plan/01` |

### 문서 경로 맵

```
docs/
├── README.md          ← 본 가이드 (문서화 규칙)
├── PRD.md             ← SSOT — 요구사항 §1~§8
├── test_cases.md      ← TC 목록 (TC-MS-001 형식)
└── defect_list.md     ← ISS/DEF 결함 목록

Report/NN_세션제목.md      ← 작업 보고서 (§1~§8)
Prompting/NN_세션제목.md   ← 프롬프트 이력 Transcript
plan/NN_세션제목.md          ← 구현 Plan (선행 분석)
```

---

## 2. 문서 종류별 자동 생성 (Auto Generation)

AI에게 아래 프롬프트로 각 문서를 생성·갱신한다.

| 문서 | 프롬프트 예시 | 저장 경로 |
|------|---------------|-----------|
| **PRD** | "§1~§8 구조로 작성해줘" | `docs/PRD.md` |
| **Test Case** | "TC-MS-001 작성해줘" | `docs/test_cases.md` |
| **Defect List** | "defect_list.md에 정리해줘" | `docs/defect_list.md` |
| **Work Report** | "Report 폴더에 생성해줘" | `Report/NN_세션제목.md` |
| **Prompt History** | "Prompting에 Export 해줘" | `Prompting/NN_세션제목.md` |

### 파일명 규칙

| 항목 | 규칙 |
|------|------|
| `NN` | 2자리 순번 (`01`, `02`, …). 기존 최대값 +1 |
| `세션제목` | 세션 주제 요약 (공백 없이 `-` 연결 권장) |
| 번호 일치 | 동일 세션의 Report·Prompting은 **같은 NN·세션제목** 사용 |

**예시**

- `Report/03_TDD-GREEN-REFACTOR-구현.md`
- `Prompting/03_TDD-GREEN-REFACTOR-구현.md`

---

## 3. 최종 보고서 8섹션 (Report/NN.md)

`Report/NN_세션제목.md`는 아래 **8개 섹션**을 반드시 포함한다.  
이 8섹션은 **Concept → Code → Result** 추적 기록이며, C2C(Concept to Code)를 문서로 닫는다.

| § | 섹션 | 내용 |
|---|------|------|
| **§1** | 작업 개요 (Work Overview) | 세션 목표·범위·상태 |
| **§2** | 완료 To-Do (Completed To-Do) | 산출물·파일 목록 |
| **§3** | RED 결과 (RED Results) | 실패 TC·스켈레톤·미구현 상태 |
| **§4** | GREEN 결과 (GREEN Results) | 통과 TC·구현 커밋·기능 완료 |
| **§5** | REFACTOR 결과 (REFACTOR Results) | 구조 개선·DRY·정리 내역 |
| **§6** | 커버리지 현황 (Coverage Status) | pytest 결과·FR/NFR 매핑 |
| **§7** | 미완료 & 다음 단계 (Incomplete & Next Steps) | 잔여 작업·우선순위 |
| **§8** | 이슈 & 결함 (Issues & Defects) | ISS/DEF + 근본 원인 |

> 기존 Report 중 §1~§8 미적용 문서는 세션 종료 시 위 구조로 정렬·갱신한다.

---

## 4. PRD §1~§8 구조

요구사항 SSOT인 [`PRD.md`](./PRD.md)는 아래 8섹션을 따른다.

| § | 섹션 |
|---|------|
| §1 | 프로젝트 개요 |
| §2 | 기본 요구사항 (FR) |
| §3 | 비즈니스 로직 |
| §4 | 품질 요구사항 (NFR) |
| §5 | 추가 요구사항 |
| §6 | Target Architecture |
| §7 | 테스트 전략 (TC) |
| §8 | Activities & 완료 기준 |

---

## 5. 현재 세션 인덱스

| NN | 세션 | Report | Prompting | 상태 |
|----|------|--------|-----------|------|
| 01 | 레거시분석·아키텍처·Plan 수립 | [Report/01](../Report/01_레거시분석-아키텍처-Plan수립.md) | [Prompting/01](../Prompting/01_레거시분석-아키텍처-Plan수립.md) | 완료 |
| 02 | TDD RED pytest 스켈레톤 | [Report/02](../Report/02_TDD-RED-pytest-스켈레톤.md) | [Prompting/02](../Prompting/02_TDD-RED-pytest-스켈레톤.md) | 완료 |
| 03 | TDD GREEN·REFACTOR 구현 | [Report/03](../Report/03_TDD-GREEN-REFACTOR-구현.md) | [Prompting/03](../Prompting/03_TDD-GREEN-REFACTOR-구현.md) | 완료 |
| 04 | Golden Master Safe Refactor | [Report/04](../Report/04_Golden-Master-Safe-Refactor.md) | [Prompting/04](../Prompting/04_Golden-Master-Safe-Refactor.md) | 완료 |
| 05 | Activity 4 추가 요구사항 확인 | [Report/05](../Report/05_Activity4-추가요구사항-확인.md) | [Prompting/05](../Prompting/05_Activity4-추가요구사항-확인.md) | 완료 |
| 06 | 단위변환 GUI·테스트 | [Report/06](../Report/06_단위변환-GUI-테스트.md) | [Prompting/06](../Prompting/06_단위변환-GUI-테스트.md) | 완료 |
| 07 | 클래스·메소드 역할 주석 | [Report/07](../Report/07_클래스-메소드-역할-주석.md) | [Prompting/07](../Prompting/07_클래스-메소드-역할-주석.md) | 완료 |
| 08 | Mom Test UX 검증 | [Report/08](../Report/08_Mom-Test-UX검증.md) | [Prompting/08](../Prompting/08_Mom-Test-UX검증.md) | 완료 |
| 09 | UX 보강·YAML config | [Report/09](../Report/09_UX보강-YAML-config.md) | [Prompting/09](../Prompting/09_UX보강-YAML-config.md) | 완료 |
| 10 | Activity 5 보강 완료 (통합 Export) | [Report/10](../Report/10_Activity5-보강-완료.md) | [Prompting/10](../Prompting/10_Activity5-보강-완료.md) | 완료 |

---

## 6. 관련 링크

- [PRD (SSOT)](./PRD.md)
- [테스트 케이스 목록](./test_cases.md)
- [결함 목록](./defect_list.md)
- [프로젝트 README](../README.md) — 실행 방법·개요 (요구사항은 PRD 참조)
