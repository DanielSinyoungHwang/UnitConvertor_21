from unit_converter.domain.exceptions import UnknownUnitError
from unit_converter.domain.length_unit import LengthUnit, MetersPerUnitLengthUnit

DEFAULT_METERS_PER_UNIT = {
    "meter": 1.0,
    "feet": 1.0 / 3.28084,
    "yard": 1.0 / 1.09361,
}


class UnitRegistry:
    def __init__(self, *, with_defaults: bool = True) -> None:
        self._units: dict[str, LengthUnit] = {}
        if with_defaults:
            for name, meters_per_unit in DEFAULT_METERS_PER_UNIT.items():
                self.register(MetersPerUnitLengthUnit(name, meters_per_unit))

    def register(self, unit: LengthUnit) -> None:
        self._units[unit.name] = unit

    def lookup(self, name: str) -> LengthUnit:
        try:
            return self._units[name]
        except KeyError:
            raise UnknownUnitError(name) from None

    def all_units(self) -> list[LengthUnit]:
        return list(self._units.values())
