"""
Golden Master — legacy UnitConverter.py 동작 고정

| ID   | 테스트                         | 추출 대상                    |
|------|--------------------------------|------------------------------|
| GM-01| 콜론 구분 파싱                 | app/input_parser.py          |
| GM-02| float 변환                     | app/input_parser.py          |
| GM-03| meter/feet/yard 단위 인식      | domain/unit_registry.py      |
| GM-04| 미지원 단위 거부               | domain/unit_registry.py      |
| GM-05| meter 허브 변환 (legacy if/elif)| domain/unit_registry.py     |
| GM-06| 공백 trim 후 파싱              | app/input_parser.py          |
"""

import pytest

from tests.legacy_golden_master import (
    legacy_is_known_unit,
    legacy_parse_float,
    legacy_split_input,
    legacy_to_meter,
)


class TestGoldenMasterInputParser:
    """app/input_parser.py — legacy 파싱 동작 보존"""

    @pytest.fixture
    def registry(self):
        from unit_converter.infrastructure.config_loader import load_registry

        return load_registry()

    def test_gm01_colon_split_matches_legacy(self, registry):
        from unit_converter.app.input_parser import parse_and_validate

        for raw, expected_unit, expected_value in [
            ("meter:2.5", "meter", 2.5),
            ("feet:8.2", "feet", 8.2),
            ("yard:1.0", "yard", 1.0),
        ]:
            legacy = legacy_split_input(raw)
            assert legacy is not None
            unit, value = parse_and_validate(raw, registry)
            assert unit == legacy[0].strip() == expected_unit
            assert value == expected_value

    def test_gm02_float_parsing_matches_legacy(self, registry):
        from unit_converter.app.input_parser import parse_and_validate

        for raw in ("meter:2.5", "feet:0", "yard:100"):
            _, value_str = legacy_split_input(raw)
            legacy_value = legacy_parse_float(value_str)
            _, parsed_value = parse_and_validate(raw, registry)
            assert parsed_value == legacy_value

    def test_gm06_whitespace_trim_beyond_legacy(self, registry):
        from unit_converter.app.input_parser import parse_and_validate

        unit, value = parse_and_validate(" meter:2.5 ", registry)
        assert unit == "meter"
        assert value == 2.5


class TestGoldenMasterRegistry:
    """domain/unit_registry.py — legacy if/elif 단위 목록 보존"""

    @pytest.fixture
    def registry(self):
        from unit_converter.infrastructure.config_loader import load_registry

        return load_registry()

    def test_gm03_known_units_match_legacy(self, registry):
        for unit in ("meter", "feet", "yard"):
            assert legacy_is_known_unit(unit)
            assert registry.lookup(unit).name == unit

    def test_gm04_unknown_unit_rejected_like_legacy(self, registry):
        from unit_converter.domain.exceptions import UnknownUnitError

        assert not legacy_is_known_unit("cubit")
        with pytest.raises(UnknownUnitError):
            registry.lookup("cubit")

    def test_gm05_to_meter_matches_legacy_if_elif(self, registry):
        cases = [
            ("meter", 2.5),
            ("feet", 8.2),
            ("yard", 1.0),
        ]
        for unit, value in cases:
            legacy_meters = legacy_to_meter(unit, value)
            unit_obj = registry.lookup(unit)
            assert unit_obj.to_meter(value) == pytest.approx(legacy_meters)

    def test_gm07_default_registry_matches_config_loader(self):
        from unit_converter.domain.unit_registry import create_default_registry
        from unit_converter.infrastructure.config_loader import load_registry

        default = create_default_registry()
        loaded = load_registry()

        for unit in ("meter", "feet", "yard"):
            assert default.lookup(unit).to_meter(1.0) == pytest.approx(
                loaded.lookup(unit).to_meter(1.0)
            )
