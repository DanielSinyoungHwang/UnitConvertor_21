# UnitConvertor_21 — 레거시 분석·아키텍처·Plan 수립 보고서

**작성일:** 2026-06-11
**프로젝트:** UnitConvertor_21
**세션:** 1단계 — 문제 코드 분석 + Target Architecture·Plan 문서화
**상태:** 완료 (구현 미착수)

---

## 1. 세션 목표

1. [README.md](../README.md) PRD 대비 [UnitConverter.py](../UnitConverter.py) **레거시 스멜·PRD 갭** 목록화
2. **Target Architecture** 기반 OCP/SRP Python 패키지 구조 제안
3. **FR 7건 · NFR 7건** 모듈 매핑
4. **Mom Test** 체크포인트 정의
5. 프로젝트 [plan/01.md](../plan/01.md) 및 Cursor plan 동기화

---

## 2. 산출물

| 파일 | 설명 |
|------|------|
| [plan/01.md](../plan/01.md) | 리팩터링 Plan (워크스페이스) |
| `.cursor/plans/레거시_스멜_prd_갭_9805c203.plan.md` | Cursor Plan (상세본) |
| `Report/01_레거시분석-아키텍처-Plan수립.md` | 본 통합 보고서 |
| `Prompting/01_레거시분석-아키텍처-Plan수립.md` | 통합 Transcript |

**코드 변경:** 없음 (`UnitConverter.py` 레거시 유지)

---

## 3. 핵심 결정

### 3.1 분석

- 레거시 스멜 **16건**, PRD 충족도 약 **30%** (meter 기반 변환만)
- PRD 갭: 기본 2부분·2미충족, 품질 2미충족·1부분, 추가 3건 미구현

### 3.2 아키텍처 (Target Architecture)

```
unit_converter/
├── domain/          length_unit, unit_registry, converter, exceptions
├── infrastructure/  config_loader (JSON/YAML)
├── app/             input_parser, output_formatter, registration_parser
├── cli.py
└── tests/           test_converter (Track B), test_cli (Track A)
```

- **OCP:** `LengthUnit` Protocol + `UnitRegistry` — `converter.py` 수정 없이 단위 확장
- **SRP:** Parser / Registry / Converter / Formatter / Config Load / CLI 분리
- **Mom Test:** 2·4단계 완료 후 선택 진행 (현재 불필요)

### 3.3 구현 순서

Activity 2 → Mom Test 확인 → Activity 3 (pytest) → Activity 4 → Mom Test 확인

---

## 4. 검증 결과

| 항목 | 결과 |
|------|------|
| 저장소 | `UnitConverter.py`, `README.md` (+ plan/Report/Prompting) |
| 테스트·설정 | `test_*.py`, JSON/YAML 없음 |
| pytest | 미실시 |
| 비즈니스 로직 | `3.28084`, `1.09361` PRD 일치 (하드코딩) |
| FR/NFR | 7+7 매핑 완료 |
| Mom Test | 2단계 구현 전 — SKIP |

### 레거시 스멜 요약 (16건)

- 구조/설계 4 · 코드 품질 4 · 입력/출력 5 · 프로젝트 3

### PRD 갭 요약

| 구분 | 상태 |
|------|------|
| 기본 요구 | 2건 부분, 2건 미충족 |
| 품질 요구 | OCP/SRP 미충족, 검증 부분 |
| 추가 요구 | 3건 전부 미구현 |
| Activities 2~4 | 미달 |

---

## 5. AI 활용 회고

- **도움이 된 순간:**
  - README → PRD 테이블 대조, L16–32 근거로 OCP/DRY 구체화
  - Target Architecture 슬라이드와 PRD 요구 정합
  - 레거시 스멜 → Target 모듈 해소 매핑
  - Mom Test vs pytest 역할 분리

- **한계·주의점:**
  - Plan mode — 패키지 스캐폴딩·pytest 미실행
  - 반올림·동일 단위 출력 UX는 구현 시 확정

---

## 6. 다음 액션

- [ ] Activity 2: `domain/` (length_unit, unit_registry, converter, exceptions)
- [ ] Activity 2: `app/input_parser.py`, `cli.py`, `__main__.py`
- [ ] Mom Test 진행 여부 확인 (2단계 완료 후)
- [ ] Activity 3: `tests/test_converter.py`, `tests/test_cli.py`
- [ ] Activity 4: config_loader, registration_parser, output_formatter
- [ ] (선택) `UnitConverter.py` thin wrapper

---

## 7. 관련 문서

- [plan/01.md](../plan/01.md)
- [Prompting/01_레거시분석-아키텍처-Plan수립.md](../Prompting/01_레거시분석-아키텍처-Plan수립.md)
- [README.md](../README.md)
