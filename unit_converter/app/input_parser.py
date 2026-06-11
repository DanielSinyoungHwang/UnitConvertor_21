from unit_converter.domain.exceptions import UnknownUnitError
from unit_converter.domain.unit_registry import UnitRegistry


class InputFormatError(Exception):
    pass


class InvalidNumberError(Exception):
    def __init__(self, value: str) -> None:
        self.value = value
        super().__init__(f"Invalid number: {value}")


class NegativeValueError(Exception):
    pass


def parse_and_validate(input_str: str, registry: UnitRegistry) -> tuple[str, float]:
    unit, value_str = _parse_input(input_str)
    value = _validate_value(value_str)
    _validate_unit(unit, registry)
    return unit, value


def _parse_input(input_str: str) -> tuple[str, str]:
    input_str = input_str.strip()

    if ":" not in input_str:
        raise InputFormatError("Invalid format. Use unit:value (ex: meter:2.5)")

    unit, value_str = input_str.split(":", 1)
    return unit.strip(), value_str


def _validate_value(value_str: str) -> float:
    try:
        value = float(value_str)
    except ValueError as exc:
        raise InvalidNumberError(value_str) from exc

    if value < 0:
        raise NegativeValueError()

    return value


def _validate_unit(unit: str, registry: UnitRegistry) -> None:
    try:
        registry.lookup(unit)
    except UnknownUnitError:
        raise
