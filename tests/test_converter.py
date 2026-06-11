"""
Track B — Domain (Dual-Track)

| ID  | 테스트                              | 대상 모듈              | FR/NFR        |
|-----|-------------------------------------|------------------------|---------------|
| B-01| meter → feet 변환 (반올림 1자리)    | domain/converter.py    | FR-02, FR-04  |
| B-02| meter → yard 변환 (반올림 1자리)    | domain/converter.py    | FR-02, FR-04  |
| B-03| feet → meter 변환                     | domain/converter.py    | FR-04         |
| B-04| feet → yard (meter 허브 경유)         | domain/converter.py    | FR-04         |
| B-05| yard → feet (meter 허브 경유)         | domain/converter.py    | FR-04         |
| B-06| 입력 단위 제외, 나머지 단위만 반환    | domain/converter.py    | FR-02         |
| B-07| meter/feet/yard registry 등록·조회    | domain/unit_registry.py| FR-03         |
| B-08| 미등록 단위 조회 시 예외              | domain/exceptions.py   | NFR-03        |
| B-09| 새 단위 등록 후 converter 수정 없이 변환 | domain/converter.py | NFR-01 (OCP) |
| B-10| LengthUnit Protocol 계약 (name, to_meter) | domain/length_unit.py | FR-04    |
"""

import pytest


class TestConverter:
    """domain/converter.py — meter 허브 변환 (I/O 무관)"""

    @pytest.fixture
    def converter(self):
        from unit_converter.domain.converter import Converter
        from unit_converter.domain.unit_registry import UnitRegistry

        return Converter(UnitRegistry())

    def test_b01_meter_to_feet_rounded_one_decimal(self, converter):
        result = converter.convert("meter", 2.5)
        assert result["feet"] == 8.2

    def test_b02_meter_to_yard_rounded_one_decimal(self, converter):
        result = converter.convert("meter", 2.5)
        assert result["yard"] == 2.7

    def test_b03_feet_to_meter(self, converter):
        result = converter.convert("feet", 8.2)
        assert result["meter"] == 2.5

    def test_b04_feet_to_yard_via_meter_hub(self, converter):
        result = converter.convert("feet", 1.0)
        assert result["yard"] == 0.3

    def test_b05_yard_to_feet_via_meter_hub(self, converter):
        result = converter.convert("yard", 1.0)
        assert result["feet"] == 3.0

    def test_b06_excludes_source_unit_from_results(self, converter):
        result = converter.convert("meter", 2.5)
        assert "meter" not in result
        assert set(result.keys()) == {"feet", "yard"}


class TestUnitRegistry:
    """domain/unit_registry.py — OCP 핵심"""

    def test_b07_registers_meter_feet_yard(self):
        from unit_converter.domain.unit_registry import UnitRegistry

        registry = UnitRegistry()
        assert registry.lookup("meter").name == "meter"
        assert registry.lookup("feet").name == "feet"
        assert registry.lookup("yard").name == "yard"

    def test_b09_new_unit_without_modifying_converter(self):
        from unit_converter.domain.converter import Converter
        from unit_converter.domain.length_unit import MetersPerUnitLengthUnit
        from unit_converter.domain.unit_registry import UnitRegistry

        registry = UnitRegistry()
        registry.register(MetersPerUnitLengthUnit("cubit", 0.4572))
        converter = Converter(registry)
        result = converter.convert("cubit", 1.0)
        assert "meter" in result
        assert result["meter"] == 0.5


class TestDomainExceptions:
    """domain/exceptions.py"""

    def test_b08_raises_for_unknown_unit(self):
        from unit_converter.domain.exceptions import UnknownUnitError
        from unit_converter.domain.unit_registry import UnitRegistry

        registry = UnitRegistry()
        with pytest.raises(UnknownUnitError):
            registry.lookup("cubit")


class TestLengthUnitProtocol:
    """domain/length_unit.py — Protocol 계약"""

    def test_b10_length_unit_has_name_and_to_meter(self):
        from unit_converter.domain.length_unit import LengthUnit, MetersPerUnitLengthUnit

        unit = MetersPerUnitLengthUnit("meter", 1.0)
        assert unit.name == "meter"
        assert unit.to_meter(2.5) == 2.5
        assert unit.from_meter(2.5) == 2.5
        assert isinstance(unit, LengthUnit)
