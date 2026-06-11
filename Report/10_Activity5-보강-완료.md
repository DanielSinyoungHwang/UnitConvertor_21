# UnitConvertor_21 — Activity 5 보강 완료 보고서

**작성일:** 2026-06-11  
**프로젝트:** UnitConvertor_21  
**세션:** Activity 5 — Cursor rule · Mom Test · TC · UX · YAML · 문서 동기화  
**상태:** 완료

---

## 1. 세션 목표

- Cursor rule/skill 필요성 검토 및 프로젝트 rule 추가
- RED 전 Mom Test 등 **보강 포인트** 식별·일괄 구현
- Mom Test 소급 수행, 에러 경로 TC·GUI smoke test 보강
- Report/08·09 분할 산출을 본 Export(10)로 통합 정리

---

## 2. 산출물

| 파일 | 설명 |
|------|------|
| `.cursor/rules/unit-converter.mdc` | PRD SSOT·아키텍처·TDD·Mom Test·Export 규칙 |
| `Report/08_Mom-Test-UX검증.md` | Mom Test CLI/GUI 검증, UX-001~004 제안 |
| `Report/09_UX보강-YAML-config.md` | UX 구현·YAML config |
| `Prompting/07_클래스-메소드-역할-주석.md` | Report/07 소급 Transcript |
| `Prompting/08_Mom-Test-UX검증.md` | Mom Test 세션 Transcript |
| `Prompting/09_UX보강-YAML-config.md` | UX·YAML Transcript |
| `tests/test_cli.py` | A-12~A-15 추가 |
| `tests/test_gui_smoke.py` | GUI smoke 4건 + module-scoped tk fixture |
| `config/units.yaml` | FR-06 YAML 설정 |
| `unit_converter/cli.py` | UX-001~004 프롬프트·메시지·등록 분기 |
| `unit_converter/domain/exceptions.py` | Unknown unit 등록 힌트 |
| `unit_converter/app/registration_parser.py` | `looks_like_registration_attempt()` |
| `unit_converter/app/output_formatter.py` | `SUPPORTED_FORMATS` |
| `unit_converter/infrastructure/config_loader.py` | JSON·YAML 파싱 |
| `requirements-dev.txt` | `pyyaml>=6.0` |
| `README.md` | CLI·format·GUI·pytest 실행 예시 |
| `plan/01_*.md` | 현재 상태·Todo 체크 갱신 |
| `docs/PRD.md` | 36 TC, Mom Test·YAML 완료 반영 |
| `docs/test_cases.md` | A-12~A-15, G01~G04 |
| `docs/defect_list.md` | ISS-001~004 CLOSED |
| `docs/README.md` | 세션 인덱스 07~10 |

---

## 3. 핵심 결정

### 3.1 Cursor rule vs skill

- **rule 1개** 권장·구현 (`.cursor/rules/unit-converter.mdc`, alwaysApply)
- **프로젝트 skill** 불필요 — `/export` 커맨드·PRD·Report/Prompting으로 충분

### 3.2 Mom Test 타이밍

- RED 전 Mom Test **SKIP** — Plan대로 정상
- 2·4단계 후 Mom Test **미실시**가 실제 갭 → Report/08에서 소급 검증

### 3.3 UX-001~004 (Report/09)

| ID | 구현 |
|----|------|
| UX-001 | CLI 프롬프트에 등록 예시 추가 |
| UX-002 | `Unknown unit` 시 `To register: 1 {unit} = <ratio> meter` |
| UX-003 | `looks_like_registration_attempt` — 등록 유사 입력 분기 |
| UX-004 | `Supported: csv, json, table` |

### 3.4 YAML (FR-06)

- `config/units.yaml` + `config_loader` 확장자 분기
- 기본 로드 경로 `units.json` 유지
- PyYAML은 `requirements-dev.txt` 의존성

---

## 4. 검증 결과

```bash
python -m pytest -q
# 36 passed in 0.27s
```

| Track | TC | 결과 |
|-------|-----|------|
| A (Boundary/CLI) | 15 | PASS |
| B (Domain) | 10 | PASS |
| GM (Golden Master) | 7 | PASS |
| GUI smoke | 4 | PASS |

| 결함 | 최종 상태 |
|------|-----------|
| ISS-001 YAML | CLOSED |
| ISS-002 Mom Test | CLOSED |
| ISS-003 Prompting/07 | CLOSED |
| ISS-004 CLI UX | CLOSED |

**OPEN 이슈:** 없음

---

## 5. AI 활용 회고

- **도움이 된 순간:**
  - Plan·PRD의 Mom Test 체크포인트를 기준으로 “RED 전 SKIP vs 2·4단계 후 누락”을 명확히 분리
  - Mom Test UX 이슈 → TC(A-15) + 메시지 개선으로 연결해 재발 방지
  - 분할 Report(08·09) 후 `/export`로 세션 전체를 10번에 통합 정리

- **한계·주의점:**
  - Mom Test는 비개발자 시뮬레이션 — 발표 시 1명 5분 재검증 권장
  - GUI smoke는 tkinter 환경 의존 — module-scoped fixture로 다중 Tk 오류 완화

---

## 6. 다음 액션

- [ ] Activity 5 회고·발표 (PRD §8 Activities 완료)
- [ ] (선택) 실제 비개발자 Mom Test 5분 재검증

---

## 7. 관련 문서

- `Prompting/10_Activity5-보강-완료.md`
- `Report/08_Mom-Test-UX검증.md`
- `Report/09_UX보강-YAML-config.md`
- `docs/PRD.md` §8.1
