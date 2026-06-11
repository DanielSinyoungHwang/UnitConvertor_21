# UnitConvertor_21 — TDD RED pytest 스켈레톤 보고서

**작성일:** 2026-06-11
**프로젝트:** UnitConvertor_21
**세션:** 3단계(Activity 3) — TDD RED 단계
**상태:** 완료 (구현 미착수)

---

## 1. 세션 목표

- [plan/01_레거시분석-아키텍처-Plan수립.md](../plan/01_레거시분석-아키텍처-Plan수립.md) 기준 **Dual-Track** pytest 스켈레톤 작성
- TDD **RED** 단계만 수행 — `pytest.fail` 사용, **구현 금지**
- Track B(Domain) + Track A(Boundary/CLI) TC 골격 확정

---

## 2. 산출물

| 파일 | 설명 |
|------|------|
| [tests/test_converter.py](../tests/test_converter.py) | Track B — Domain TC 10건 (B-01~B-10) |
| [tests/test_cli.py](../tests/test_cli.py) | Track A — Boundary/CLI TC 11건 (A-01~A-11) |
| [tests/__init__.py](../tests/__init__.py) | tests 패키지 |
| [requirements-dev.txt](../requirements-dev.txt) | pytest 의존성 |
| [Prompting/02_TDD-RED-pytest-스켈레톤.md](../Prompting/02_TDD-RED-pytest-스켈레톤.md) | 본 세션 Transcript |

**코드 변경:** `unit_converter/` 패키지·도메인·CLI **미생성** (의도적)

---

## 3. 핵심 결정

### 3.1 Dual-Track TC 구성

| Track | 파일 | 범위 | TC 수 |
|-------|------|------|-------|
| **B** | `test_converter.py` | `domain/` — 변환·registry·Protocol·예외 | 10 |
| **A** | `test_cli.py` | `app/`·`cli.py`·`infrastructure/` 경계 | 11 |

- 각 파일 module docstring에 **Dual-Track 표**(ID·테스트·대상 모듈·FR/NFR) 포함
- Activity 3 핵심(B-01~B-10, A-01~A-07) + Activity 4 선행 스켈레톤(A-08~A-11) 포함

### 3.2 RED 스켈레톤 규칙

- 모든 테스트는 `pytest.fail("RED: ...")` 로만 종료
- 미구현 모듈 import 없음 → 수집(collect) 단계 오류 방지
- Given 주석으로 GREEN 단계 Assert 의도 명시

### 3.3 구현 순서 (Plan 연계)

```
현재(RED) → Activity 2 구현(GREEN) → Activity 4 확장(GREEN) → REFACTOR
```

---

## 4. 검증 결과

```bash
python -m pip install -q pytest
python -m pytest -v --tb=no
```

| 항목 | 결과 |
|------|------|
| 수집 TC | 21건 |
| 통과 | 0 |
| 실패(RED) | **21** |
| 소요 | 0.11s |
| 환경 | Python 3.14.4, pytest 9.0.3, win32 |

**판정:** 전 TC FAILED — TDD RED 상태 정상 확인

---

## 5. AI 활용 회고

- **도움이 된 순간:**
  - Plan §3 Target Architecture·FR/NFR 매핑 → Dual-Track 표 직접 전환
  - `pytest.fail`만 사용해 import 오류 없이 RED 유지
  - Activity 3/4 범위를 Track A에 단계별 분리

- **한계·주의점:**
  - GREEN 전환 시 `pytest.fail` → Arrange-Act-Assert 교체 필요
  - 반올림·동일 단위 제외(B-06)는 README/레거시 갭 기준 — 구현 시 확정
  - Mom Test: domain/CLI 미구현 — **SKIP** (2단계 완료 후 확인 예정)

---

## 6. 다음 액션

- [ ] Activity 2: `domain/` (`length_unit`, `unit_registry`, `converter`, `exceptions`)
- [ ] Activity 2: `app/input_parser.py`, `cli.py`, `__main__.py`
- [ ] Mom Test 진행 여부 확인 (2단계 완료 후)
- [ ] GREEN: Track B TC (B-01~B-10) `pytest.fail` 제거·Assert 구현
- [ ] GREEN: Track A TC (A-01~A-07) `pytest.fail` 제거·Assert 구현
- [ ] Activity 4: config_loader, registration_parser, output_formatter + A-08~A-11 GREEN

---

## 7. 관련 문서

- [plan/01_레거시분석-아키텍처-Plan수립.md](../plan/01_레거시분석-아키텍처-Plan수립.md)
- [Prompting/02_TDD-RED-pytest-스켈레톤.md](../Prompting/02_TDD-RED-pytest-스켈레톤.md)
- [Report/01_레거시분석-아키텍처-Plan수립.md](01_레거시분석-아키텍처-Plan수립.md)
- [README.md](../README.md)
