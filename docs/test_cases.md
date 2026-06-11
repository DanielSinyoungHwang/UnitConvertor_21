# UnitConvertor_21 — Test Cases

**형식:** TC-MS-NNN (Master TC) · B-NN (Domain Track) · A-NN (Boundary Track) · GM-NN (Golden Master)  
**SSOT:** 요구사항 매핑은 [`PRD.md`](./PRD.md) §7 참조  
**구현:** `tests/test_converter.py`, `tests/test_cli.py`, `tests/test_golden_master.py`

---

## Track B — Domain (`test_converter.py`)

| TC ID | Given | When | Then | FR/NFR | 상태 |
|-------|-------|------|------|--------|------|
| **TC-MS-B01** (B-01) | registry에 meter/feet/yard 등록 | 2.5 meter → feet 변환 | 8.2 feet (반올림 1자리) | FR-02, FR-04 | ✅ PASS |
| **TC-MS-B02** (B-02) | registry에 meter/feet/yard 등록 | 2.5 meter → yard 변환 | 2.7 yard (반올림 1자리) | FR-02, FR-04 | ✅ PASS |
| **TC-MS-B03** (B-03) | registry에 meter/feet/yard 등록 | feet → meter 변환 | meter 기준 정확 변환 | FR-04 | ✅ PASS |
| **TC-MS-B04** (B-04) | registry에 meter/feet/yard 등록 | feet → yard 변환 | meter 허브 경유 정확 변환 | FR-04 | ✅ PASS |
| **TC-MS-B05** (B-05) | registry에 meter/feet/yard 등록 | yard → feet 변환 | meter 허브 경유 정확 변환 | FR-04 | ✅ PASS |
| **TC-MS-B06** (B-06) | registry에 meter/feet/yard 등록 | meter:2.5 변환 요청 | meter 제외 feet·yard만 반환 | FR-02 | ✅ PASS |
| **TC-MS-B07** (B-07) | 빈 registry | meter/feet/yard 등록·조회 | 3단위 정상 등록·lookup | FR-03 | ✅ PASS |
| **TC-MS-B08** (B-08) | registry에 기본 단위만 | unknown 단위 lookup | `UnknownUnitError` 발생 | NFR-03 | ✅ PASS |
| **TC-MS-B09** (B-09) | 기본 registry + cubit 등록 | cubit 변환 | converter 수정 없이 변환 성공 | NFR-01 | ✅ PASS |
| **TC-MS-B10** (B-10) | `MetersPerUnitLengthUnit` 인스턴스 | name·to_meter 접근 | Protocol 계약 충족 | FR-04 | ✅ PASS |

---

## Track A — Boundary/CLI (`test_cli.py`)

| TC ID | Given | When | Then | FR/NFR | 상태 |
|-------|-------|------|------|--------|------|
| **TC-MS-A01** (A-01) | CLI 실행, stdin `meter:2.5` | E2E 변환 | table 형식 변환 출력 | FR-01, FR-02 | ✅ PASS |
| **TC-MS-A02** (A-02) | CLI 실행 | `meter2.5` (콜론 없음) | 에러·거부 | NFR-03 | ✅ PASS |
| **TC-MS-A03** (A-03) | CLI 실행 | `meter:abc` | 에러·거부 | NFR-03 | ✅ PASS |
| **TC-MS-A04** (A-04) | CLI 실행 | `meter:-1` | 에러·거부 | NFR-03 | ✅ PASS |
| **TC-MS-A05** (A-05) | CLI 실행 | `cubit:1` (미등록) | 에러·거부 | NFR-03 | ✅ PASS |
| **TC-MS-A06** (A-06) | CLI 실행 | `  meter:2.5  ` (공백) | trim 후 정상 파싱 | FR-01 | ✅ PASS |
| **TC-MS-A07** (A-07) | CLI 실행, 기본 옵션 | `meter:2.5` | table 포맷 출력 | FR-02, FR-07 | ✅ PASS |
| **TC-MS-A08** (A-08) | `--format json` | `meter:2.5` | JSON 배열/객체 출력 | FR-07 | ✅ PASS |
| **TC-MS-A09** (A-09) | `--format csv` | `meter:2.5` | CSV 헤더+행 출력 | FR-07 | ✅ PASS |
| **TC-MS-A10** (A-10) | CLI 실행 | `1 cubit = 0.4572 meter` 등록 후 `cubit:1` | 등록·변환 성공 | FR-05 | ✅ PASS |
| **TC-MS-A11** (A-11) | `config/units.json` 존재 | `load_registry()` | meter/feet/yard 로드 | FR-06 | ✅ PASS |
| **TC-MS-A12** (A-12) | CLI/GUI 등록 파서 | `cubit = 1 meter`, `1 cubit = 0.4572 meters` | `RegistrationFormatError` | FR-05 | ✅ PASS |
| **TC-MS-A13** (A-13) | CLI `run()` | `output_format="xml"` | `Unsupported format: xml. Supported: csv, json, table` | FR-07 | ✅ PASS |
| **TC-MS-A14** (A-14) | `config/units.yaml` 존재 | `load_registry(yaml_path)` | meter/feet/yard 동일 비율 | FR-06 | ✅ PASS |
| **TC-MS-A15** (A-15) | CLI | `cubit = 1 meter` | 등록 형식 오류 (변환 오류 아님) | FR-05 | ✅ PASS |

---

## GUI Smoke (`test_gui_smoke.py`)

| TC ID | Given | When | Then | 상태 |
|-------|-------|------|------|------|
| **TC-MS-G01** | GUI + registry | meter 2.5 변환 | feet·yard 2행 표시 | ✅ PASS |
| **TC-MS-G02** | GUI | meter:-1 변환 | 상태바 음수 오류 | ✅ PASS |
| **TC-MS-G03** | GUI | 잘못된 등록 형식 | messagebox 오류 | ✅ PASS |
| **TC-MS-G04** | GUI | cubit 등록 후 변환 | 3단위 결과 | ✅ PASS |

---

## Golden Master (`test_golden_master.py`)

| TC ID | Given | When | Then | 상태 |
|-------|-------|------|------|------|
| **TC-MS-GM01** (GM-01) | 레거시 파서 동작 | input_parser 동일 입력 | 동일 파싱 결과 | ✅ PASS |
| **TC-MS-GM02** (GM-02) | 레거시 변환 비율 | converter 동일 입력 | 동일 변환 결과 | ✅ PASS |
| **TC-MS-GM03** (GM-03) | 레거시 registry 시드 | load_registry | 3단위 동일 비율 | ✅ PASS |
| **TC-MS-GM04~07** | 레거시 E2E 케이스 | CLI 경로 | 레거시 출력 보존 | ✅ PASS |

---

## 실행

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -v
# 36 passed
```

### TC 추가 프롬프트

```
TC-MS-A12 작성해줘
```

→ 본 문서에 TC 정의 추가 후 `tests/test_cli.py`에 구현.
