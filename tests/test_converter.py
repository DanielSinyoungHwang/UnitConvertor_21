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

    def test_b01_meter_to_feet_rounded_one_decimal(self):
        # Given: meter 2.5 → feet ≈ 8.2021 → 8.2 (README 기준 반올림)
        pytest.fail("RED: domain/converter.py — meter→feet 변환 미구현 (B-01)")

    def test_b02_meter_to_yard_rounded_one_decimal(self):
        # Given: meter 2.5 → yard ≈ 2.734 → 2.7
        pytest.fail("RED: domain/converter.py — meter→yard 변환 미구현 (B-02)")

    def test_b03_feet_to_meter(self):
        # Given: feet 8.2 → meter (meter 허브 역산)
        pytest.fail("RED: domain/converter.py — feet→meter 변환 미구현 (B-03)")

    def test_b04_feet_to_yard_via_meter_hub(self):
        # Given: feet 1.0 → yard (feet→meter→yard, if/elif 없음)
        pytest.fail("RED: domain/converter.py — feet→yard 허브 변환 미구현 (B-04)")

    def test_b05_yard_to_feet_via_meter_hub(self):
        # Given: yard 1.0 → feet (yard→meter→feet)
        pytest.fail("RED: domain/converter.py — yard→feet 허브 변환 미구현 (B-05)")

    def test_b06_excludes_source_unit_from_results(self):
        # Given: meter:2.5 입력 시 결과에 meter 자기 자신 미포함
        pytest.fail("RED: domain/converter.py — 입력 단위 제외 로직 미구현 (B-06)")


class TestUnitRegistry:
    """domain/unit_registry.py — OCP 핵심"""

    def test_b07_registers_meter_feet_yard(self):
        # Given: 기본 3단위 등록 후 lookup 성공
        pytest.fail("RED: domain/unit_registry.py — 기본 단위 등록·조회 미구현 (B-07)")

    def test_b09_new_unit_without_modifying_converter(self):
        # Given: cubit 등록 후 converter.py 수정 없이 변환 가능 (OCP)
        pytest.fail("RED: domain/unit_registry.py + converter.py — OCP 확장 미구현 (B-09)")


class TestDomainExceptions:
    """domain/exceptions.py"""

    def test_b08_raises_for_unknown_unit(self):
        # Given: registry에 없는 단위 조회 시 도메인 예외
        pytest.fail("RED: domain/exceptions.py — UnknownUnitError 미구현 (B-08)")


class TestLengthUnitProtocol:
    """domain/length_unit.py — Protocol 계약"""

    def test_b10_length_unit_has_name_and_to_meter(self):
        from unit_converter.domain.length_unit import LengthUnit, MetersPerUnitLengthUnit

        unit = MetersPerUnitLengthUnit("meter", 1.0)
        assert unit.name == "meter"
        assert unit.to_meter(2.5) == 2.5
        assert unit.from_meter(2.5) == 2.5
        assert isinstance(unit, LengthUnit)
