from unit_converter.domain.exceptions import UnknownUnitError
from unit_converter.domain.length_unit import LengthUnit


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
