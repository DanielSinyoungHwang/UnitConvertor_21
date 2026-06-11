"""LengthUnit 등록·조회를 담당하는 단위 레지스트리."""

from unit_converter.domain.exceptions import UnknownUnitError
from unit_converter.domain.length_unit import LengthUnit, MetersPerUnitLengthUnit

# Legacy UnitConverter.py if/elif 단위 — Golden Master baseline
_LEGACY_METERS_PER_UNIT: dict[str, float] = {
    "meter": 1.0,
    "feet": 1.0 / 3.28084,
    "yard": 1.0 / 1.09361,
}


def create_default_registry() -> "UnitRegistry":
    """레거시 3단위를 registry에 시드 (Activity 2 추출 결과)."""
    registry = UnitRegistry()
    for name, meters_per_unit in _LEGACY_METERS_PER_UNIT.items():
        registry.register(MetersPerUnitLengthUnit(name, meters_per_unit))
    return registry


class UnitRegistry:
    """이름으로 LengthUnit을 등록·조회·열거하는 단위 저장소."""

    def __init__(self) -> None:
        """빈 단위 딕셔너리로 레지스트리를 초기화한다."""
        self._units: dict[str, LengthUnit] = {}

    def register(self, unit: LengthUnit) -> None:
        """단위를 이름 키로 레지스트리에 추가(또는 덮어쓰기)한다."""
        self._units[unit.name] = unit

    def lookup(self, name: str) -> LengthUnit:
        """이름으로 단위를 조회한다. 미등록 시 UnknownUnitError."""
        try:
            return self._units[name]
        except KeyError:
            raise UnknownUnitError(name) from None

    def all_units(self) -> list[LengthUnit]:
        """등록된 모든 단위 목록을 반환한다."""
        return list(self._units.values())
