from unit_converter.domain.unit_registry import UnitRegistry


class Converter:
    def __init__(self, registry: UnitRegistry) -> None:
        self._registry = registry

    def convert(self, source_unit: str, value: float) -> dict[str, float]:
        source = self._registry.lookup(source_unit)
        meters = source.to_meter(value)
        results: dict[str, float] = {}
        for unit in self._registry.all_units():
            if unit.name == source_unit:
                continue
            results[unit.name] = round(unit.from_meter(meters), 1)
        return results
