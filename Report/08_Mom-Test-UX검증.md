# UnitConvertor_21 — Mom Test UX 검증 보고서

**작성일:** 2026-06-11  
**프로젝트:** UnitConvertor_21  
**세션:** Activity 5 — Mom Test (2·4단계 체크포인트 소급)  
**상태:** 완료

---

## 1. 세션 목표

Plan §6·PRD §7.3에 정의된 **Mom Test 체크포인트**(2단계 CLI·에러 UX, 4단계 포맷·동적 등록 UX)를 소급 수행하고, 비개발자 관점에서의 이슈를 기록한다.

---

## 2. 검증 방법

| 항목 | 내용 |
|------|------|
| 검증자 | 개발자가 Mom Test 질문 스크립트로 **비개발자 시나리오 시뮬레이션** |
| 대상 | CLI (`python -m unit_converter`), GUI (`python -m unit_converter.gui`) |
| 보조 | `tests/test_gui_smoke.py` — GUI 연동 smoke test 4건 |
| 소요 | 약 15분 |

### Mom Test 질문 스크립트

1. "길이를 다른 단위로 바꾸려면 뭘 입력해야 할 것 같아?"
2. "이 출력이 무슨 뜻인지 설명해 줄 수 있어?"
3. "잘못 입력했을 때 무엇이 문제인지 알겠어?"
4. "새 단위를 등록하려면 어떻게 해야 할 것 같아?"
5. "JSON/CSV 출력을 실제로 쓸 수 있을 것 같아?"

---

## 3. CLI 검증 결과

| # | 시나리오 | 입력/명령 | 관찰 | Mom Test 판정 |
|---|----------|-----------|------|---------------|
| 1 | 정상 변환 | `meter:2.5` | `2.5 meter = 8.2 feet` 형식 직관적 | ✅ PASS |
| 2 | 형식 오류 | `meter2.5` | `Invalid format. Use unit:value (ex: meter:2.5)` — 예시 포함으로 수정 방법 명확 | ✅ PASS |
| 3 | 음수 | `meter:-1` | `Negative values are not allowed.` — 이유는 알 수 있음 | ✅ PASS |
| 4 | 미등록 단위 | `cubit:1` | `Unknown unit: cubit` — 등록 필요성은 암시되나 **등록 방법은 안내 없음** | ⚠️ 개선 여지 |
| 5 | JSON 출력 | `--format json` | 구조화되어 파싱 가능; 비개발자에게는 table이 더 친숙 | ✅ PASS (대상 사용자별) |
| 6 | 동적 등록 | `1 cubit = 0.4572 meter` → `cubit:1` | 등록 후 재입력 흐름은 자연스러움; **형식 예시는 프롬프트에 없음** | ⚠️ 개선 여지 |
| 7 | 잘못된 등록 | `cubit = 1 meter` | 변환 형식 오류로 처리됨 (`unit:value` 안내) — **등록 형식 오류와 혼동 가능** | ⚠️ 개선 여지 |
| 8 | 미지원 포맷 | `--format xml` | `Unsupported format: xml` — 지원 목록(table/json/csv) 미안내 | ⚠️ 개선 여지 |

---

## 4. GUI 검증 결과

| # | 시나리오 | 관찰 | 판정 |
|---|----------|------|------|
| 1 | 변환 패널 | 값·단위 콤보·변환 버튼 — 레이블 한글로 직관적 | ✅ PASS |
| 2 | unit:value 입력 | "또는 unit:value" 보조 경로 제공 | ✅ PASS |
| 3 | 단위 등록 | placeholder `예: 1 cubit = 0.4572 meter` — CLI보다 안내 우수 | ✅ PASS |
| 4 | 오류 표시 | 상태바·messagebox로 피드백 | ✅ PASS |
| 5 | smoke test | `test_gui_smoke.py` 4 passed — 도메인 연동 정상 | ✅ PASS |

---

## 5. 발견 이슈 (UX)

| ID | 심각도 | 내용 | 권장 |
|----|--------|------|------|
| UX-001 | 낮음 | CLI 프롬프트에 등록 형식 예시 없음 | `_PROMPT`에 등록 예시 1줄 추가 (선택) |
| UX-002 | 낮음 | `Unknown unit` 시 등록 힌트 없음 | 메시지에 `1 name = N meter` 힌트 (선택) |
| UX-003 | 낮음 | 잘못된 등록 입력이 변환 형식 오류로 처리 | `is_registration_input` 완화 또는 휴리스틱 (선택) |
| UX-004 | 낮음 | 미지원 `--format` 시 지원 목록 미표시 | `Supported: table, json, csv` 추가 (선택) |

→ 기능 결함이 아닌 **UX 개선 제안**. pytest 30건 통과, FR/NFR 충족 유지.

---

## 6. 검증 결과 (pytest)

```bash
python -m pytest -v
# 32 passed (기존 28 + A-12/A-13 + GUI smoke 4)
```

| Track | TC | 결과 |
|-------|-----|------|
| B (Domain) | 10 | PASS |
| A (Boundary/CLI) | 13 | PASS (+A-12, A-13) |
| GM (Golden Master) | 7 | PASS |
| GUI smoke | 4 | PASS |

---

## 7. AI 활용 회고

- **도움이 된 순간:** Plan에 정의된 Mom Test 체크포인트를 소급 적용해, pytest가 잡지 못하는 “메시지 혼동”을 UX-003으로 분리 기록
- **한계·주의점:** 실제 비개발자 참여 없이 시뮬레이션 — 발표 시 1명에게 5분 재검증 권장

---

## 8. 다음 액션

- [x] Mom Test Report 작성
- [x] A-12/A-13 에러 경로 TC
- [x] GUI smoke test
- [ ] (선택) UX-001~004 메시지 개선

---

## 9. 관련 문서

- `Prompting/08_Mom-Test-UX검증.md`
- `plan/01_레거시분석-아키텍처-Plan수립.md` §6
- `docs/PRD.md` §7.3, §8.1
