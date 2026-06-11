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
| A-12| 잘못된 등록 형식 거부                 | app/registration_parser.py   | FR-05      |
| A-13| 미지원 --format 거부                  | cli.py                       | FR-07      |
| A-14| units.yaml 설정 로드                  | infrastructure/config_loader | FR-06      |
| A-15| 등록 유사 잘못된 입력 거부            | cli.py + registration_parser | FR-05      |
"""

import pytest


class TestInputParser:
    """app/input_parser.py — 경계 입력 검증"""

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

    def test_a01_valid_input_produces_conversion_output(self, capsys, monkeypatch):
        from unit_converter.cli import main

        monkeypatch.setattr("builtins.input", lambda _: "meter:2.5")
        main()
        out = capsys.readouterr().out
        assert "feet" in out
        assert "yard" in out

    def test_a07_default_table_format(self, capsys, monkeypatch):
        from unit_converter.cli import main

        monkeypatch.setattr("builtins.input", lambda _: "meter:2.5")
        main()
        out = capsys.readouterr().out
        assert "2.5 meter = 8.2 feet" in out
        assert "2.5 meter = 2.7 yard" in out


class TestOutputFormatter:
    """app/output_formatter.py — FR-07 (Activity 4)"""

    def test_a08_json_format_flag(self, capsys, monkeypatch):
        import json

        from unit_converter.cli import main

        monkeypatch.setattr("builtins.input", lambda _: "meter:2.5")
        monkeypatch.setattr("sys.argv", ["unit_converter", "--format", "json"])
        main()
        out = capsys.readouterr().out.strip()
        payload = json.loads(out)
        assert payload["source"] == {"unit": "meter", "value": 2.5}
        assert {"unit": "feet", "value": 8.2} in payload["conversions"]

    def test_a09_csv_format_flag(self, capsys, monkeypatch):
        from unit_converter.cli import main

        monkeypatch.setattr("builtins.input", lambda _: "meter:2.5")
        monkeypatch.setattr("sys.argv", ["unit_converter", "--format", "csv"])
        main()
        out = capsys.readouterr().out
        assert "source_unit,source_value,target_unit,target_value" in out
        assert "meter,2.5,feet,8.2" in out


class TestRegistrationParser:
    """app/registration_parser.py — FR-05 (Activity 4)"""

    def test_a10_dynamic_unit_registration(self, capsys, monkeypatch):
        from unit_converter.cli import main

        inputs = iter(["1 cubit = 0.4572 meter", "cubit:1"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        main()
        out = capsys.readouterr().out
        assert "1.0 cubit = 0.5 meter" in out

    def test_a12_rejects_invalid_registration_format(self):
        from unit_converter.app.registration_parser import (
            RegistrationFormatError,
            parse_registration,
        )

        with pytest.raises(RegistrationFormatError, match="Invalid registration format"):
            parse_registration("cubit = 1 meter")

        with pytest.raises(RegistrationFormatError):
            parse_registration("1 cubit = 0.4572 meters")


class TestCliFormatErrors:
    """cli.py — 출력 포맷 경계"""

    def test_a13_rejects_unsupported_format(self, capsys):
        from unit_converter.cli import run

        exit_code = run("meter:2.5", output_format="xml")
        out = capsys.readouterr().out
        assert exit_code == 1
        assert "Unsupported format: xml" in out
        assert "Supported: csv, json, table" in out


class TestRegistrationLikeInput:
    """등록 형식과 유사한 잘못된 입력 — UX-003"""

    def test_a15_cli_rejects_registration_like_input(self, capsys, monkeypatch):
        from unit_converter.cli import main

        monkeypatch.setattr("builtins.input", lambda _: "cubit = 1 meter")
        exit_code = main()
        out = capsys.readouterr().out
        assert exit_code == 1
        assert "Invalid registration format" in out
        assert "unit:value" not in out


class TestConfigLoader:
    """infrastructure/config_loader.py — FR-06 (Activity 4)"""

    def test_a11_loads_units_from_json_config(self, registry, converter):
        result = converter.convert("meter", 2.5)
        assert registry.lookup("meter").name == "meter"
        assert registry.lookup("feet").name == "feet"
        assert registry.lookup("yard").name == "yard"
        assert result["feet"] == 8.2
        assert result["yard"] == 2.7

    def test_a14_loads_units_from_yaml_config(self):
        from pathlib import Path

        from unit_converter.domain.converter import Converter
        from unit_converter.infrastructure.config_loader import load_registry

        yaml_path = Path("config/units.yaml")
        registry = load_registry(yaml_path)
        converter = Converter(registry)
        result = converter.convert("meter", 2.5)
        assert result["feet"] == 8.2
        assert result["yard"] == 2.7
