"""CLI/GUI 변환 입력(unit:value) 파싱 및 검증."""

from unit_converter.domain.exceptions import UnknownUnitError
from unit_converter.domain.unit_registry import UnitRegistry


class InputFormatError(Exception):
    """unit:value 형식이 아닌 입력일 때 발생."""


class InvalidNumberError(Exception):
    """값 부분이 유효한 숫자가 아닐 때 발생."""

    def __init__(self, value: str) -> None:
        """파싱에 실패한 원본 문자열을 보관한다."""
        self.value = value
        super().__init__(f"Invalid number: {value}")


class NegativeValueError(Exception):
    """음수 값이 입력되었을 때 발생."""


def parse_and_validate(input_str: str, registry: UnitRegistry) -> tuple[str, float]:
    """입력 문자열을 파싱·검증하고 (단위, 값) 튜플을 반환한다."""
    unit, value_str = _parse_input(input_str)
    value = _validate_value(value_str)
    _validate_unit(unit, registry)
    return unit, value


def _parse_input(input_str: str) -> tuple[str, str]:
    """unit:value 형식에서 단위명과 값 문자열을 분리한다."""
    input_str = input_str.strip()

    if ":" not in input_str:
        raise InputFormatError("Invalid format. Use unit:value (ex: meter:2.5)")

    unit, value_str = input_str.split(":", 1)
    return unit.strip(), value_str


def _validate_value(value_str: str) -> float:
    """값 문자열을 float로 변환하고 음수 여부를 검사한다."""
    try:
        value = float(value_str)
    except ValueError as exc:
        raise InvalidNumberError(value_str) from exc

    if value < 0:
        raise NegativeValueError()

    return value


def _validate_unit(unit: str, registry: UnitRegistry) -> None:
    """단위가 레지스트리에 등록되어 있는지 확인한다."""
    try:
        registry.lookup(unit)
    except UnknownUnitError:
        raise
