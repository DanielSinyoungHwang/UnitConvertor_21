import json
from pathlib import Path

from unit_converter.domain.length_unit import MetersPerUnitLengthUnit
from unit_converter.domain.unit_registry import UnitRegistry


def load_registry(config_path: Path) -> UnitRegistry:
    data = json.loads(config_path.read_text(encoding="utf-8"))
    base_unit = data["base_unit"]
    registry = UnitRegistry(with_defaults=False)

    for name, ratio in data["units"].items():
        if name == base_unit:
            meters_per_unit = 1.0
        else:
            meters_per_unit = 1.0 / ratio
        registry.register(MetersPerUnitLengthUnit(name, meters_per_unit))

    return registry
