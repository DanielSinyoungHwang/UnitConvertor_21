# UnitConvertor_21 — UX 보강·YAML config 보고서

**작성일:** 2026-06-11  
**프로젝트:** UnitConvertor_21  
**세션:** Report/08 잔여 — UX-001~004 · FR-06 YAML  
**상태:** 완료

---

## 1. 세션 목표

- Mom Test에서 도출된 UX-001~004 CLI 메시지 개선
- FR-06 YAML 설정 파일 지원 (`config/units.yaml`)
- ISS-001 · ISS-004 결함 종료

---

## 2. 산출물

| 파일 | 변경 |
|------|------|
| `unit_converter/cli.py` | 프롬프트 등록 예시, 등록 유사 입력 분기, format 지원 목록 |
| `unit_converter/domain/exceptions.py` | `Unknown unit` 시 등록 힌트 |
| `unit_converter/app/registration_parser.py` | `looks_like_registration_attempt()` |
| `unit_converter/app/output_formatter.py` | `SUPPORTED_FORMATS` 상수 |
| `unit_converter/infrastructure/config_loader.py` | JSON·YAML 파싱 분기 |
| `config/units.yaml` | JSON과 동일 비율 |
| `requirements-dev.txt` | `pyyaml>=6.0` |
| `tests/test_cli.py` | A-14, A-15 추가 · A-13 갱신 |
| `tests/test_gui_smoke.py` | module-scoped `tk_root` fixture 안정화 |

---

## 3. UX 개선 (Report/08 → 구현)

| ID | Before | After |
|----|--------|-------|
| UX-001 | `ex: meter:2.5` 만 | `or register unit (ex: 1 cubit = 0.4572 meter)` 추가 |
| UX-002 | `Unknown unit: cubit` | `... To register: 1 cubit = <ratio> meter` |
| UX-003 | `cubit = 1 meter` → 변환 형식 오류 | `looks_like_registration_attempt` → 등록 형식 오류 |
| UX-004 | `Unsupported format: xml` | `... Supported: csv, json, table` |

---

## 4. YAML config (FR-06)

- `load_registry(Path("config/units.yaml"))` — 확장자 `.yaml`/`.yml` 시 PyYAML `safe_load`
- 기본 경로는 `config/units.json` 유지 (기존 동작 불변)
- PyYAML 미설치 시 `ImportError`와 설치 안내 메시지

---

## 5. 검증 결과

```bash
python -m pytest -v
# 36 passed in 0.30s
```

| TC | 결과 |
|----|------|
| A-13 (format 목록) | PASS |
| A-14 (YAML 로드) | PASS |
| A-15 (등록 유사 입력) | PASS |
| GUI smoke 4건 | PASS |

---

## 6. 결함 갱신

| ID | 상태 |
|----|------|
| ISS-001 YAML config | CLOSED |
| ISS-004 CLI UX | CLOSED |

---

## 7. 관련 문서

- `Prompting/09_UX보강-YAML-config.md`
- `Report/08_Mom-Test-UX검증.md`
- `docs/PRD.md` §5, §8.1
