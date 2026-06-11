# UnitConvertor_21 — TDD GREEN·REFACTOR 구현 보고서

**작성일:** 2026-06-11
**프로젝트:** UnitConvertor_21
**세션:** Activity 2~4 — TDD GREEN + REFACTOR
**상태:** 완료

---

## 1. 세션 목표

- RED 스켈레톤(21 TC)을 **GREEN** — RED 묶음(테스트 클래스)당 1커밋, 최소 구현
- **REFACTOR** — DRY·CLI 정리·thin wrapper·gitignore, pytest 21 passed 유지
- Target Architecture(`domain/` / `app/` / `infrastructure/` / `cli`) 충족

---

## 2. 산출물

| 파일 | 설명 |
|------|------|
| `unit_converter/domain/` | `length_unit`, `exceptions`, `unit_registry`, `converter` |
| `unit_converter/app/` | `input_parser`, `output_formatter`, `registration_parser` |
| `unit_converter/infrastructure/` | `config_loader` |
| `unit_converter/cli.py`, `__main__.py` | CLI 조립 |
| `config/units.json` | 변환 비율 외부 설정 |
| `UnitConverter.py` | `cli.main()` thin wrapper (4줄) |
| `tests/conftest.py` | `registry`, `converter` 공유 fixture |
| `.gitignore` | `__pycache__`, `.pytest_cache`, `venv/` |
| [Prompting/03_TDD-GREEN-REFACTOR-구현.md](../Prompting/03_TDD-GREEN-REFACTOR-구현.md) | 본 세션 Transcript |

---

## 3. 핵심 결정

### 3.1 GREEN — RED 묶음당 1커밋 (11건)

| 커밋 | RED 묶음 | 구현 |
|------|----------|------|
| `09c1570` | B-10 | `LengthUnit` Protocol, `MetersPerUnitLengthUnit` |
| `051592a` | B-08 | `UnknownUnitError`, registry lookup 예외 |
| `af4d22d` | B-07/B-09 | `UnitRegistry`, `Converter` |
| `1735932` | B-01~B-06 | 변환 TC Assert |
| `c5a3028` | A-02~A-06 | `input_parser` |
| `1236ef6` | A-01/A-07 | `cli`, table `output_formatter` |
| `3f8990b` | A-08/A-09 | JSON/CSV 포맷 |
| `9cdb77c` | A-10 | `registration_parser`, 동적 등록 |
| `3468cc1` | A-11 | `config/units.json`, `config_loader` |

### 3.2 REFACTOR (2건)

| 커밋 | 내용 |
|------|------|
| `775dab0` | `DEFAULT_METERS_PER_UNIT` 제거 → `config/units.json` 단일 출처 (NFR-06) |
| `dec29d5` | `FORMATTERS` dict, `is_registration_input`, conftest, `UnitConverter.py` wrapper, `.gitignore`, `__pycache__` 추적 해제 |

### 3.3 아키텍처·비율 모델

- meter 허브: `to_meter = value × meters_per_unit`, `from_meter = meters / meters_per_unit`
- config JSON hub ratio → `1/ratio` 변환 (`hub_ratio_to_meters_per_unit`)
- `UnitRegistry()`는 빈 registry; 기본 단위는 `load_registry()` 경유

### 3.4 Mom Test

- **확인 필요** (Plan §6) — CLI·에러 메시지·출력 UX 최초 구현 완료
- pytest 21건으로 기능 검증 완료; 비개발자 UX 검증은 선택 진행

---

## 4. 검증 결과

```bash
python -m pytest -q
# 21 passed in 0.05s
```

| 항목 | 결과 |
|------|------|
| Track B (Domain) | 10 passed |
| Track A (Boundary/CLI) | 11 passed |
| 실행 | `python -m unit_converter`, `python UnitConverter.py`, `--format json/csv` |
| FR 7건 | 구현 완료 (테스트 매핑) |
| NFR OCP/SRP/DRY | registry+config 단일 출처, 레이어 분리 |
| git | GREEN 9 + REFACTOR 2 = **11커밋** (`49b6768` TDD RED 이후) |

---

## 5. AI 활용 회고

- **도움이 된 순간:**
  - RED 묶음 = 테스트 클래스 → 커밋 단위로 GREEN 순서 자연 정렬 (B-10→B-08→B-07…)
  - Dual-Track: domain 먼저 GREEN 후 CLI 경계 — 의존성 충돌 최소화
  - REFACTOR에서 config 단일 출처 통합 시 기존 TC 그대로 통과

- **한계·주의점:**
  - B-10 커밋에 `exceptions`/`unit_registry` 스켈레톤이 함께 포함됨 (후속 B-08 커밋은 TC 전환 위주)
  - Plan config 주석(`1 unit = ratio meter`)과 legacy hub multiplier 해석 불일치 — 구현은 README·legacy 기준
  - Mom Test 미실시

---

## 6. 다음 액션

- [ ] **Mom Test** 진행 여부 확인 (CLI 메시지·table/json/csv·동적 등록 UX)
- [ ] README 실행 예시 갱신 (`python -m unit_converter`)
- [ ] (선택) YAML config 지원 (FR-06 확장)
- [ ] Activity 5 회고·발표 준비

---

## 7. 관련 문서

- [Prompting/03_TDD-GREEN-REFACTOR-구현.md](../Prompting/03_TDD-GREEN-REFACTOR-구현.md)
- [plan/01_레거시분석-아키텍처-Plan수립.md](../plan/01_레거시분석-아키텍처-Plan수립.md)
- [Report/02_TDD-RED-pytest-스켈레톤.md](02_TDD-RED-pytest-스켈레톤.md)
- [README.md](../README.md)
