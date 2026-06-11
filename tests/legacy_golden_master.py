"""Frozen snapshot of legacy UnitConverter.py parsing & unit-dispatch logic.

Golden Master baseline — refactor 시 동작 회귀 방지용.
원본: main branch UnitConverter.py (37줄)
"""


def legacy_split_input(input_str: str) -> tuple[str, str] | None:
    if ":" not in input_str:
        return None
    unit, value_str = input_str.split(":", 1)
    return unit, value_str


def legacy_parse_float(value_str: str) -> float | None:
    try:
        return float(value_str)
    except ValueError:
        return None


def legacy_to_meter(unit: str, value: float) -> float | None:
    if unit == "meter":
        return value
    if unit == "feet":
        return value / 3.28084
    if unit == "yard":
        return value / 1.09361
    return None


def legacy_is_known_unit(unit: str) -> bool:
    return legacy_to_meter(unit, 1.0) is not None
