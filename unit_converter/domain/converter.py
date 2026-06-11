"""길이 단위 변환 도메인 서비스."""

from unit_converter.domain.unit_registry import UnitRegistry


class Converter:
    """등록된 단위 간 길이 변환을 수행하는 도메인 서비스."""

    def __init__(self, registry: UnitRegistry) -> None:
        """UnitRegistry를 주입받아 변환기를 초기화한다."""
        self._registry = registry

    def convert(self, source_unit: str, value: float) -> dict[str, float]:
        """source_unit의 value를 meter 중간값으로 환산한 뒤, 나머지 등록 단위별 변환 결과를 반환한다."""
        source = self._registry.lookup(source_unit)
        meters = source.to_meter(value)
        results: dict[str, float] = {}
        for unit in self._registry.all_units():
            if unit.name == source_unit:
                continue
            results[unit.name] = round(unit.from_meter(meters), 1)
        return results
