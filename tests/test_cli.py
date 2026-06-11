"""
Track A — Boundary / CLI (Dual-Track)

| ID  | 테스트                              | 대상 모듈                 | FR/NFR        |
|-----|-------------------------------------|---------------------------|---------------|
| A-01| 정상 입력 meter:2.5 → 변환 출력       | cli.py (E2E)              | FR-01, FR-02  |
| A-02| 콜론 없는 형식 거부                   | app/input_parser.py       | NFR-03        |
| A-03| 잘못된 숫자 거부                      | app/input_parser.py       | NFR-03        |
| A-04| 음수 값 거부                          | app/input_parser.py       | NFR-03        |
| A-05| 미지원 단위 거부                      | app/input_parser.py       | NFR-03        |
| A-06| 앞뒤 공백 trim 후 파싱                | app/input_parser.py       | FR-01         |
| A-07| 기본 table 출력 포맷                  | app/output_formatter.py   | FR-02, FR-07  |
| A-08| --format json 출력                    | cli.py + output_formatter | FR-07         |
| A-09| --format csv 출력                     | cli.py + output_formatter | FR-07         |
| A-10| 동적 단위 등록 후 변환                | app/registration_parser.py| FR-05         |
| A-11| units.json 설정 로드                  | infrastructure/config_loader | FR-06      |
"""

import pytest


class TestInputParser:
    """app/input_parser.py — 경계 입력 검증"""

    @pytest.fixture
    def registry(self):
        from unit_converter.domain.unit_registry import UnitRegistry

        return UnitRegistry()

    def test_a02_rejects_missing_colon(self, registry):
        from unit_converter.app.input_parser import InputFormatError, parse_and_validate

        with pytest.raises(InputFormatError):
            parse_and_validate("meter2.5", registry)

    def test_a03_rejects_invalid_number(self, registry):
        from unit_converter.app.input_parser import InvalidNumberError, parse_and_validate

        with pytest.raises(InvalidNumberError):
            parse_and_validate("meter:abc", registry)

    def test_a04_rejects_negative_value(self, registry):
        from unit_converter.app.input_parser import NegativeValueError, parse_and_validate

        with pytest.raises(NegativeValueError):
            parse_and_validate("meter:-2.5", registry)

    def test_a05_rejects_unknown_unit(self, registry):
        from unit_converter.domain.exceptions import UnknownUnitError
        from unit_converter.app.input_parser import parse_and_validate

        with pytest.raises(UnknownUnitError):
            parse_and_validate("cubit:1.0", registry)

    def test_a06_trims_whitespace_around_input(self, registry):
        from unit_converter.app.input_parser import parse_and_validate

        unit, value = parse_and_validate(" meter:2.5 ", registry)
        assert unit == "meter"
        assert value == 2.5


class TestCliBoundary:
    """cli.py — stdin/stdout 경계 (도메인·CLI 분리)"""

    def test_a01_valid_input_produces_conversion_output(self, capsys):
        # Given: stdin "meter:2.5" → stdout에 feet/yard 변환 줄 포함
        pytest.fail("RED: cli.py — 정상 E2E 변환 출력 미구현 (A-01)")

    def test_a07_default_table_format(self, capsys):
        # Given: 기본 실행 → "2.5 meter = 8.2 feet" 형태 table 출력
        pytest.fail("RED: app/output_formatter.py — table 포맷 미구현 (A-07)")


class TestOutputFormatter:
    """app/output_formatter.py — FR-07 (Activity 4)"""

    def test_a08_json_format_flag(self, capsys):
        # Given: --format json → JSON 구조 출력
        pytest.fail("RED: app/output_formatter.py — JSON 포맷 미구현 (A-08)")

    def test_a09_csv_format_flag(self, capsys):
        # Given: --format csv → CSV 구조 출력
        pytest.fail("RED: app/output_formatter.py — CSV 포맷 미구현 (A-09)")


class TestRegistrationParser:
    """app/registration_parser.py — FR-05 (Activity 4)"""

    def test_a10_dynamic_unit_registration(self, capsys):
        # Given: "1 cubit = 0.4572 meter" 등록 후 cubit:1 변환 가능
        pytest.fail("RED: app/registration_parser.py — 동적 단위 등록 미구현 (A-10)")


class TestConfigLoader:
    """infrastructure/config_loader.py — FR-06 (Activity 4)"""

    def test_a11_loads_units_from_json_config(self):
        # Given: config/units.json → meter/feet/yard 비율 로드
        pytest.fail("RED: infrastructure/config_loader.py — JSON 설정 로드 미구현 (A-11)")
