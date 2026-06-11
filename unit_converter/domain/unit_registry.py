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
    def __init__(self) -> None:
        self._units: dict[str, LengthUnit] = {}

    def register(self, unit: LengthUnit) -> None:
        self._units[unit.name] = unit

    def lookup(self, name: str) -> LengthUnit:
        try:
            return self._units[name]
        except KeyError:
            raise UnknownUnitError(name) from None

    def all_units(self) -> list[LengthUnit]:
        return list(self._units.values())
