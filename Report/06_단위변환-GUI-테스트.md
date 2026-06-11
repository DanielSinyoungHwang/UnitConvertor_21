# UnitConvertor_21 — 단위변환 GUI 테스트 보고서

**작성일:** 2026-06-11
**프로젝트:** UnitConvertor_21
**세션:** GUI 테스트 도구 추가
**상태:** 완료

---

## 1. 세션 목표

단위 변환 기능을 CLI 없이 시각적으로 테스트할 수 있는 GUI를 추가하고 실행한다.

---

## 2. 산출물

| 파일 | 설명 |
|------|------|
| `unit_converter/gui.py` | tkinter 기반 Unit Converter GUI (`UnitConverterApp` 클래스, `main()` 진입점) |

---

## 3. 핵심 결정

| 항목 | 결정 |
|------|------|
| GUI 프레임워크 | Python 표준 라이브러리 `tkinter` — 추가 의존성 없음 |
| 아키텍처 | 기존 `Converter`, `parse_and_validate`, `parse_registration`, `load_registry` 재사용 |
| UI 구성 | 값·단위 콤보박스 변환, `unit:value` 직접 입력, 단위 등록, Treeview 결과 표 |
| 실행 방법 | `python -m unit_converter.gui` |

---

## 4. 검증 결과

| 항목 | 결과 |
|------|------|
| 파일 생성 | `unit_converter/gui.py` (168줄) |
| Linter | 오류 없음 |
| GUI 실행 (1차) | 실패 — PowerShell `&&` 문법 오류 (`exit_code=1`) |
| GUI 실행 (2차) | 성공 — `python -m unit_converter.gui` 백그라운드 실행, 프로세스 유지 확인 |
| pytest | 본 세션에서 미실행 (GUI 전용 추가, 기존 도메인 로직 변경 없음) |

---

## 5. AI 활용 회고

- **도움이 된 순간:** 기존 `cli.py`·`input_parser`·`registration_parser` 구조를 그대로 연결해 GUI를 빠르게 구성할 수 있었음. 도메인 계층 변경 없이 앱 레이어 위에 UI만 추가.
- **한계·주의점:** Windows PowerShell 구버전에서 `&&` 연산자 미지원으로 1차 실행 실패 — `Set-Location; if (...) { } else { }` 형식으로 재시도 필요. GUI 자동화 테스트는 본 세션 범위 외.

---

## 6. 다음 액션

- [ ] README에 GUI 실행 방법(`python -m unit_converter.gui`) 추가 (선택)
- [ ] GUI 수동 테스트: 변환·등록·오류 입력(음수, 잘못된 형식) 확인
- [ ] 필요 시 GUI용 pytest 또는 smoke test 검토

---

## 7. 관련 문서

- `Prompting/06_단위변환-GUI-테스트.md`
