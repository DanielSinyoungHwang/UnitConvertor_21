# UnitConvertor_21 — Product Requirements Document (PRD)

**SSOT (Single Source of Truth)** — 요구사항은 이 문서만을 기준으로 한다.  
**작성일:** 2026-06-11  
**상태:** Activities 2~5 완료 · Mom Test · UX 보강 · YAML config · 36 TC passed

---

## §1. 프로젝트 개요

### 1.1 목적

사용자가 입력한 길이(`단위:값`)를 기반으로 해당 값을 **다른 모든 등록 단위**로 변환해 출력하는 Python 프로그램.

### 1.2 핵심 설계 목표

- 새 단위 추가 시 **기존 변환 로직(`converter.py`) 수정 최소화** (OCP)
- 파싱·변환·출력·설정 로드 **책임 분리** (SRP)
- 각 단위 변환·입력 검증을 **테스트 코드로 검증** (TDD)

### 1.3 실행 방법

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

python -m unit_converter
python -m unit_converter --format json
python UnitConverter.py        # thin wrapper
```

### 1.4 입·출력 예시

**입력**

```
meter:2.5
```

**출력 (table, 기본)**

```
2.5 meter = 8.2 feet
2.5 meter = 2.7 yard
```

---

## §2. 기본 요구사항 (Functional Requirements)

| ID | 요구사항 | 담당 모듈 | 상태 |
|----|----------|-----------|------|
| FR-01 | `단위:값` 형식 파싱 (`meter:2.5`) | `app/input_parser.py` | ✅ |
| FR-02 | 입력 단위를 제외한 **모든 등록 단위**로 변환 출력 | `domain/converter.py` + `app/output_formatter.py` | ✅ |
| FR-03 | meter / feet / yard 기본 지원 | `config/units.json` + `domain/unit_registry.py` | ✅ |
| FR-04 | meter 기준 비율로 모든 단위 간 변환 | `domain/length_unit.py` + `domain/converter.py` | ✅ |
| FR-05 | 동적 단위 등록 (`1 cubit = 0.4572 meter`) | `app/registration_parser.py` + `unit_registry.py` | ✅ |
| FR-06 | 변환 비율을 외부 설정 파일(JSON/YAML)에서 로드 | `infrastructure/config_loader.py` | ✅ (JSON·YAML) |
| FR-07 | 출력 포맷 선택 (table / JSON / CSV) | `app/output_formatter.py` + `cli.py` | ✅ |

### FR-01 상세

- 형식: `{unit_name}:{numeric_value}`
- 앞뒤 공백 trim 후 파싱
- 콜론 없음·잘못된 숫자·음수·미지원 단위 → 거부 및 에러 메시지

### FR-05 상세

- 등록 형식: `1 {new_unit} = {ratio} {base_unit}`
- 등록 성공 후 변환 입력 재요청
- 등록된 단위는 세션 내 registry에 반영

### FR-07 상세

| 포맷 | CLI 옵션 | 기본값 |
|------|----------|--------|
| table | (없음) | ✅ |
| json | `--format json` | |
| csv | `--format csv` | |

---

## §3. 비즈니스 로직

### 3.1 변환 비율 (meter 허브)

| 단위 | 비율 |
|------|------|
| 1 meter | = 1.0 meter (기준) |
| 1 feet | = 3.28084 meter (config: hub ratio → meters_per_unit 변환) |
| 1 yard | = 1.09361 meter |

- feet/yard 간 비율은 **meter 기준**으로 계산
- config JSON의 `units` 값: `1 {unit} = {ratio} meter`

### 3.2 변환 알고리즘

```
to_meter   = value × meters_per_unit(source)
from_meter = meters / meters_per_unit(target)
```

### 3.3 출력 정밀도

- 소수점 **반올림 1자리** (예: `8.2 feet`, `2.7 yard`)

---

## §4. 품질 요구사항 (Non-Functional Requirements)

| ID | 요구사항 | 충족 방식 | 상태 |
|----|----------|-----------|------|
| NFR-01 | OCP | `LengthUnit` Protocol + `UnitRegistry`; `converter.py` 불변 | ✅ |
| NFR-02 | SRP | Parser / Registry / Converter / Formatter / Config / CLI 분리 | ✅ |
| NFR-03 | 입력 검증 | `app/input_parser.py` — 형식·숫자·음수·미지원 단위 | ✅ |
| NFR-04 | 테스트 코드 | Track B (Domain) + Track A (Boundary/CLI) | ✅ |
| NFR-05 | 테스트 가능 구조 | domain 계층 I/O 무관, fixture 주입 | ✅ |
| NFR-06 | DRY | `config/units.json` 단일 출처 (하드코딩 제거) | ✅ |
| NFR-07 | CLI·도메인 분리 | `cli.py`는 조립·I/O만 담당 | ✅ |

---

## §5. 추가 요구사항

| # | 요구사항 | 구현 | TC |
|---|----------|------|-----|
| 1 | **설정 외부화** — JSON/YAML에서 비율 로드 | `config/units.json`, `config_loader.py` | A-11 |
| 2 | **동적 단위 등록** — 런타임 registry 확장 | `registration_parser.py`, `cli.py` | A-10 |
| 3 | **출력 포맷 선택** — table / json / csv | `output_formatter.py`, `--format` | A-07~A-09 |

### 미구현·선택 항목

- GUI (`unit_converter/gui.py`) — 교육용 확장, CLI PRD 범위 외 (smoke test 4건)

---

## §6. Target Architecture

```
unit_converter/
├── domain/          length_unit, unit_registry, converter, exceptions
├── infrastructure/  config_loader
├── app/             input_parser, output_formatter, registration_parser
├── cli.py, __main__.py, gui.py
└── tests/           test_converter (Track B), test_cli (Track A)

config/units.json    ← 비율 SSOT (NFR-06)
UnitConverter.py     ← cli.main() thin wrapper
```

### 6.1 OCP

```
새 단위 =
  (A) LengthUnit 구현 + registry.register()
  (B) units.json 1줄 추가 → config_loader 시드
→ converter.py 수정 금지
```

### 6.2 SRP — 책임 분리

| 책임 | 모듈 |
|------|------|
| Parser | `app/input_parser.py` |
| Registry | `domain/unit_registry.py` |
| Converter | `domain/converter.py` |
| Formatter | `app/output_formatter.py` |
| Config Load | `infrastructure/config_loader.py` |
| CLI | `cli.py` |

### 6.3 레이어 의존

```
cli.py → app/ → domain/
cli.py → infrastructure/ → domain/ → config/units.json
```

---

## §7. 테스트 전략 (TC)

### 7.1 Dual-Track 구성

| Track | 파일 | 범위 | TC 수 |
|-------|------|------|-------|
| **B** (Domain) | `tests/test_converter.py` | 변환·registry·Protocol·예외 | 10 |
| **A** (Boundary) | `tests/test_cli.py` | 파싱·CLI·포맷·등록·설정·에러 경로 | 15 |
| **GM** (Golden Master) | `tests/test_golden_master.py` | 레거시 동작 보존 | 7 |
| **GUI** (Smoke) | `tests/test_gui_smoke.py` | GUI·도메인 연동 | 4 |

**현재:** `36 passed` (2026-06-11)

### 7.2 TC 목록

상세 TC 정의는 [`test_cases.md`](./test_cases.md) 참조.

| ID | 테스트 요약 | FR/NFR |
|----|-------------|--------|
| B-01 | meter → feet (반올림 1자리) | FR-02, FR-04 |
| B-02 | meter → yard (반올림 1자리) | FR-02, FR-04 |
| B-03 | feet → meter | FR-04 |
| B-04 | feet → yard (meter 허브) | FR-04 |
| B-05 | yard → feet (meter 허브) | FR-04 |
| B-06 | 입력 단위 제외 나머지 반환 | FR-02 |
| B-07 | meter/feet/yard registry 등록·조회 | FR-03 |
| B-08 | 미등록 단위 조회 시 예외 | NFR-03 |
| B-09 | 새 단위 등록 후 converter 수정 없이 변환 | NFR-01 |
| B-10 | LengthUnit Protocol 계약 | FR-04 |
| A-01 | 정상 입력 meter:2.5 → 변환 출력 | FR-01, FR-02 |
| A-02 | 콜론 없는 형식 거부 | NFR-03 |
| A-03 | 잘못된 숫자 거부 | NFR-03 |
| A-04 | 음수 값 거부 | NFR-03 |
| A-05 | 미지원 단위 거부 | NFR-03 |
| A-06 | 앞뒤 공백 trim 후 파싱 | FR-01 |
| A-07 | 기본 table 출력 포맷 | FR-02, FR-07 |
| A-08 | `--format json` 출력 | FR-07 |
| A-09 | `--format csv` 출력 | FR-07 |
| A-10 | 동적 단위 등록 후 변환 | FR-05 |
| A-11 | units.json 설정 로드 | FR-06 |
| A-12 | 잘못된 등록 형식 거부 | FR-05 |
| A-13 | 미지원 `--format` 거부 | FR-07 |
| A-14 | units.yaml 설정 로드 | FR-06 |
| A-15 | 등록 유사 잘못된 입력 거부 | FR-05 |

### 7.3 Mom Test 체크포인트

| 시점 | 판단 |
|------|------|
| 2단계 완료 후 | ✅ 완료 — [Report/08](../Report/08_Mom-Test-UX검증.md) |
| 4단계 완료 후 | ✅ 완료 — [Report/08](../Report/08_Mom-Test-UX검증.md) |

---

## §8. Activities & 완료 기준

교육 과정 **생성형 AI 활용 Activities (6시간)** 기준.

| Activity | 내용 | 시간 | 완료 기준 | 상태 |
|----------|------|------|-----------|------|
| 1 | 문제 코드·기본 요구사항 분석 | 0.5h | 레거시 스멜·PRD 갭 목록화 | ✅ |
| 2 | 기본·품질 요구사항 구현 | 2h | OCP/SRP·입력 검증·domain/app/cli | ✅ |
| 3 | TC 구현 (TDD RED→GREEN) | 0.5h | Track A+B 21 TC passed | ✅ |
| 4 | 추가 요구사항 구현 | 2h | 설정·동적 등록·출력 포맷 + TC | ✅ |
| 5 | 회고 및 발표 | 1h | Report·Prompting·PRD 정리 | ✅ |

### 8.1 완료 판정 체크리스트

- [x] FR-01 ~ FR-07 충족
- [x] NFR-01 ~ NFR-07 충족
- [x] `python -m pytest` 36 passed
- [x] `UnitConverter.py` thin wrapper
- [x] `config/units.json` 단일 비율 출처
- [x] Mom Test — CLI/출력 UX 검증 ([Report/08](../Report/08_Mom-Test-UX검증.md))
- [x] YAML config 지원 (`config/units.yaml`, PyYAML)

### 8.2 관련 문서

| 문서 | 경로 |
|------|------|
| 문서화 가이드 | [docs/README.md](./README.md) |
| 테스트 케이스 | [docs/test_cases.md](./test_cases.md) |
| 결함 목록 | [docs/defect_list.md](./defect_list.md) |
| 구현 Plan | [plan/01_레거시분석-아키텍처-Plan수립.md](../plan/01_레거시분석-아키텍처-Plan수립.md) |
