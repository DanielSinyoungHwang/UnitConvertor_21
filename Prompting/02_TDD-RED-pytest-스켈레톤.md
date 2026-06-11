# Export Transcript — UnitConvertor_21 TDD RED pytest 스켈레톤

**Exported:** 2026-06-11
**Session:** 3단계(Activity 3) — TDD RED pytest 스켈레톤 작성

---

## Turn 1 — User

> @plan/01_레거시분석-아키텍처-Plan수립.md 파일 참고하고,
> pytest RED 스켈레톤만 작성해줘. 구현은 금지. Dual-Track 표 기준, pytest.fail 사용.
> ARRR 사이클 중 red 동작에 맞는 것만 진행해줘.

---

## Turn 1 — Agent

- `plan/01_레거시분석-아키텍처-Plan수립.md`, README, UnitConverter.py 분석
- Dual-Track 기준 RED 스켈레톤 생성 (구현 없음):

| 파일 | 내용 |
|------|------|
| `tests/test_converter.py` | Track B — B-01~B-10 (10건) |
| `tests/test_cli.py` | Track A — A-01~A-11 (11건) |
| `tests/__init__.py` | 빈 패키지 |
| `requirements-dev.txt` | `pytest>=8.0` |

- 모든 TC: `pytest.fail("RED: ...")` + Given 주석
- module docstring에 Dual-Track 표(FR/NFR 매핑) 포함
- `unit_converter/` 패키지·도메인·CLI 코드 **미생성**

**pytest 검증:**

```bash
python -m pip install -q pytest
python -m pytest -v --tb=no
# → 21 failed in 0.11s (RED 정상)
```

---

## Turn 2 — User

> `/export` (Cursor Command: export)

---

## Turn 2 — Agent

- `Report/02_TDD-RED-pytest-스켈레톤.md` 생성
- `Prompting/02_TDD-RED-pytest-스켈레톤.md` 생성 (본 파일)
- git commit 없음

---

## Session State

| 항목 | 값 |
|------|-----|
| 프로젝트 | UnitConvertor_21 |
| 단계 | Activity 3 RED 완료 — **Activity 2 구현 대기** |
| 아키텍처 | Target Architecture (domain/app/infrastructure/cli) — 미구현 |
| TC | Track B 10 + Track A 11 = **21건 RED** |
| pytest | 21 failed (RED 정상) |
| Mom Test | SKIP (2단계 구현 전) |
| 코드 변경 | tests/ + requirements-dev.txt만 추가 |
| Export | `02_TDD-RED-pytest-스켈레톤` |

---

## Prompting Context (재개용)

```
프로젝트: UnitConvertor_21
단계: Activity 3 RED 완료 — Activity 2 GREEN 대기
완료:
  - Dual-Track pytest RED 스켈레톤 (21 TC)
  - tests/test_converter.py (B-01~B-10)
  - tests/test_cli.py (A-01~A-11)
  - pytest 21 failed 확인
  - Export: Report/02_TDD-RED-pytest-스켈레톤.md
진행 중: 없음
다음:
  - Activity 2: domain/ + app/input_parser + cli.py (GREEN)
  - Mom Test 진행 여부 확인 (2단계 완료 후)
  - pytest.fail → Assert 교체 (Track B 우선)
  - Activity 4: config/infra/app 확장 + A-08~A-11 GREEN
참고: plan/01_레거시분석-아키텍처-Plan수립.md, Report/02_TDD-RED-pytest-스켈레톤.md
```
