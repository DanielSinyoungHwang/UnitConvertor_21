import json
from pathlib import Path

from unit_converter.domain.length_unit import MetersPerUnitLengthUnit
from unit_converter.domain.unit_registry import UnitRegistry

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "units.json"


def hub_ratio_to_meters_per_unit(name: str, base_unit: str, ratio: float) -> float:
    if name == base_unit:
        return 1.0
    return 1.0 / ratio


def load_registry(config_path: Path | None = None) -> UnitRegistry:
    path = config_path or DEFAULT_CONFIG_PATH
    data = json.loads(path.read_text(encoding="utf-8"))
    registry = UnitRegistry()
    base_unit = data["base_unit"]

    for name, ratio in data["units"].items():
        meters_per_unit = hub_ratio_to_meters_per_unit(name, base_unit, ratio)
        registry.register(MetersPerUnitLengthUnit(name, meters_per_unit))

    return registry
