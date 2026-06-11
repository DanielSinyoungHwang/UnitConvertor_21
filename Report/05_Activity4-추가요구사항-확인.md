# UnitConvertor_21 — Activity 4 추가 요구사항 확인 보고서

**작성일:** 2026-06-11
**프로젝트:** UnitConvertor_21
**세션:** Activity 4 — units.json · 동적 등록 · 출력 포맷 + TC 확인
**상태:** 완료

---

## 1. 세션 목표

- `config/units.json` 설정 로드(FR-06) 구현 여부 확인
- 동적 단위 등록 CLI(FR-05) 구현 여부 확인
- `--format json|csv|table` 출력 포맷(FR-07) 및 관련 TC(A-07~A-11) 존재·통과 여부 확인

---

## 2. 산출물

| 파일 | 설명 |
|------|------|
| *(코드 변경 없음)* | `expand` 브랜치에 Activity 4 구현·TC가 이미 존재함을 확인 |
| `Report/05_Activity4-추가요구사항-확인.md` | 본 보고서 |
| `Prompting/05_Activity4-추가요구사항-확인.md` | 세션 Transcript |

**확인된 기존 구현**

| 요구사항 | 모듈 | TC |
|----------|------|-----|
| units.json 로드 | `config/units.json`, `infrastructure/config_loader.py`, `cli.py` | A-11 |
| 동적 단위 등록 | `app/registration_parser.py`, `cli.py` | A-10 |
| table 출력 (기본) | `app/output_formatter.py`, `cli.py` | A-07 |
| `--format json` | `app/output_formatter.py`, `cli.py` | A-08 |
| `--format csv` | `app/output_formatter.py`, `cli.py` | A-09 |

---

## 3. 핵심 결정

- **신규 구현 불필요** — GREEN 커밋(`3468cc1`, `9cdb77c`, `3f8990b`, `1236ef6`) 및 REFACTOR(`775dab0`, `dec29d5`)에서 Activity 4가 이미 완료된 상태
- CLI는 `load_registry()`로 `units.json`을 로드하고, 첫 입력이 등록 형식(`1 cubit = 0.4572 meter`)이면 등록 후 변환 입력을 재요청
- 출력 포맷은 `FORMATTERS` dict(`table`/`json`/`csv`)로 분기, 기본값 `table`

---

## 4. 검증 결과

```bash
python -m pytest tests/test_cli.py -v
# → 11 passed in 0.05s

python -m pytest -v
# → 28 passed in 0.08s
```

| TC | 결과 |
|----|------|
| A-07 default table | PASSED |
| A-08 `--format json` | PASSED |
| A-09 `--format csv` | PASSED |
| A-10 동적 단위 등록 | PASSED |
| A-11 units.json 로드 | PASSED |

**브랜치:** `expand` (working tree clean)

---

## 5. AI 활용 회고

- **도움이 된 순간:** 코드베이스 탐색·pytest 일괄 실행으로 “미구현”이 아닌 “이미 GREEN” 상태를 빠르게 판별
- **한계·주의점:** 사용자 요청이 “추가 구현”처럼 읽혀도, 기존 GREEN·REFACTOR 이력과 TC 통과 여부를 먼저 확인해야 중복 작업을 피할 수 있음

---

## 6. 다음 액션

- [ ] Mom Test 진행 여부 확인 (Plan §6)
- [ ] (선택) 모듈 단위 TC 분리 — `test_config_loader.py`, `test_output_formatter.py`, `test_registration_parser.py`
- [ ] (선택) 에러 경로 TC — 잘못된 등록 형식, 지원하지 않는 `--format`
- [ ] (선택) `unit_registry.py` 레거시 `_LEGACY_METERS_PER_UNIT` 정리 (Golden Master GM-07과 연동)

---

## 7. 관련 문서

- `Prompting/05_Activity4-추가요구사항-확인.md`
- `plan/01_레거시분석-아키텍처-Plan수립.md`
- `Report/03_TDD-GREEN-REFACTOR-구현.md`
- `Report/04_Golden-Master-Safe-Refactor.md`
