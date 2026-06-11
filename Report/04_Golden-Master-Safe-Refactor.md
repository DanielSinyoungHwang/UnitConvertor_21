# UnitConvertor_21 — Golden Master Safe Refactor 보고서

**작성일:** 2026-06-11
**프로젝트:** UnitConvertor_21
**세션:** Golden Master 확보 + input_parser·registry Safe Refactor
**상태:** 완료

---

## 1. 세션 목표

- 레거시 `UnitConverter.py` 동작을 **Golden Master** 테스트로 고정
- **Safe Refactor** — `app/input_parser.py`, `domain/unit_registry.py` 추출·정리
- 기존 Dual-Track TC 21건 + Golden Master 7건 **회귀 없이 통과**

---

## 2. 산출물

| 파일 | 설명 |
|------|------|
| [tests/legacy_golden_master.py](../tests/legacy_golden_master.py) | 레거시 파싱·if/elif 단위 분기 스냅샷 |
| [tests/test_golden_master.py](../tests/test_golden_master.py) | Golden Master TC 7건 (GM-01~GM-07) |
| [unit_converter/app/input_parser.py](../unit_converter/app/input_parser.py) | `_parse_input` / `_validate_value` / `_validate_unit` SRP 분리 |
| [unit_converter/domain/unit_registry.py](../unit_converter/domain/unit_registry.py) | `create_default_registry()` 팩토리 추가 |
| [Prompting/04_Golden-Master-Safe-Refactor.md](../Prompting/04_Golden-Master-Safe-Refactor.md) | 본 세션 Transcript |

---

## 3. 핵심 결정

### 3.1 Golden Master 전략

- 레거시 37줄 스크립트의 **파싱·단위 분기**만 `legacy_golden_master.py`에 동결
- 전체 E2E(출력 포맷·반올림·자기 단위 제외)는 PRD 개선 범위 — GM은 **추출 대상(input_parser, registry)** 에만 적용
- GM-06: 레거시에 없던 공백 trim은 **의도적 개선** — 별도 TC로 검증

### 3.2 input_parser 추출 (SRP)

```
parse_and_validate()
  ├── _parse_input()      — strip, 콜론 분리, unit trim
  ├── _validate_value()   — float 변환, 음수 거부
  └── _validate_unit()    — registry.lookup() 위임
```

- `cli.py`는 조립만 — 파싱·검증 로직 없음

### 3.3 registry 추출 (OCP)

- `UnitRegistry`: `register` / `lookup` / `all_units`
- `create_default_registry()`: 레거시 if/elif 3단위(meter/feet/yard) 시드
- `load_registry()` (config_loader): JSON 기반 확장 — GM-07로 두 경로 **to_meter 일치** 검증

### 3.4 Mom Test

- **SKIP** — domain/app 내부 리팩터링, CLI UX 변경 없음
- pytest 28건으로 충분

---

## 4. 검증 결과

```bash
python -m pytest -q
# 28 passed in 0.06s
```

| 항목 | 결과 |
|------|------|
| Track B (Domain) | 10 passed |
| Track A (Boundary/CLI) | 11 passed |
| Golden Master | 7 passed (GM-01~GM-07) |
| 브랜치 | `refactor` |
| 커밋 | `0b89d92` refactor, golden master |

---

## 5. AI 활용 회고

- **도움이 된 순간:**
  - 레거시 if/elif → `legacy_to_meter()` 스냅샷으로 GM 비교 기준 명확화
  - input_parser 3함수 분리로 A-02~A-06 TC 수정 없이 통과
  - `create_default_registry()` vs `load_registry()` GM-07로 config·레거시 일관성 확인

- **한계·주의점:**
  - GREEN 단계에서 이미 추출된 모듈 — GM은 **회귀 방지망** 역할
  - `_LEGACY_METERS_PER_UNIT`과 `config/units.json` 이중 출처 — GM-07로 동기화만 검증, 장기적으로 config 단일 출처(NFR-06) 유지 필요

---

## 6. 다음 액션

- [ ] **Mom Test** 진행 여부 확인 (Plan §6 — 2·4단계 후)
- [ ] README 실행 예시 갱신
- [ ] (선택) converter·output_formatter Golden Master 확장
- [ ] Activity 5 회고·발표 준비

---

## 7. 관련 문서

- [Prompting/04_Golden-Master-Safe-Refactor.md](../Prompting/04_Golden-Master-Safe-Refactor.md)
- [Report/03_TDD-GREEN-REFACTOR-구현.md](03_TDD-GREEN-REFACTOR-구현.md)
- [plan/01_레거시분석-아키텍처-Plan수립.md](../plan/01_레거시분석-아키텍처-Plan수립.md)
