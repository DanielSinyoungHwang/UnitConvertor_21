"""units.json / units.yaml 설정 파일에서 UnitRegistry를 구성."""

import json
from pathlib import Path
from typing import Any

from unit_converter.domain.length_unit import MetersPerUnitLengthUnit
from unit_converter.domain.unit_registry import UnitRegistry

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "units.json"


def hub_ratio_to_meters_per_unit(name: str, base_unit: str, ratio: float) -> float:
    """base_unit 대비 ratio를 1단위당 meter 비율로 변환한다."""
    if name == base_unit:
        return 1.0
    return 1.0 / ratio


def _load_config_data(path: Path) -> dict[str, Any]:
    """설정 파일 확장자에 따라 JSON 또는 YAML을 파싱한다."""
    text = path.read_text(encoding="utf-8")
    suffix = path.suffix.lower()

    if suffix in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError as exc:
            raise ImportError(
                "YAML config requires PyYAML. Install with: pip install pyyaml"
            ) from exc
        data = yaml.safe_load(text)
    else:
        data = json.loads(text)

    if not isinstance(data, dict):
        raise ValueError(f"Config root must be a mapping: {path}")

    return data


def _build_registry(data: dict[str, Any]) -> UnitRegistry:
    """파싱된 설정 dict로 UnitRegistry를 구성한다."""
    registry = UnitRegistry()
    base_unit = data["base_unit"]

    for name, ratio in data["units"].items():
        meters_per_unit = hub_ratio_to_meters_per_unit(name, base_unit, ratio)
        registry.register(MetersPerUnitLengthUnit(name, meters_per_unit))

    return registry


def load_registry(config_path: Path | None = None) -> UnitRegistry:
    """설정 파일을 읽어 단위가 등록된 UnitRegistry를 반환한다."""
    path = config_path or DEFAULT_CONFIG_PATH
    return _build_registry(_load_config_data(path))
