"""동적 단위 등록 입력(1 cubit = 0.4572 meter) 파싱."""

import re

from unit_converter.domain.length_unit import MetersPerUnitLengthUnit

_REGISTRATION_PATTERN = re.compile(
    r"^\s*1\s+(\w+)\s*=\s*([0-9.]+)\s+meter\s*$",
    re.IGNORECASE,
)


class RegistrationFormatError(Exception):
    """등록 형식(1 name = N meter)이 아닌 입력일 때 발생."""


_REGISTRATION_LIKE_PATTERN = re.compile(
    r"\w+\s*=\s*[0-9.]+\s+meters?",
    re.IGNORECASE,
)


def is_registration_input(input_str: str) -> bool:
    """입력이 단위 등록 형식인지 여부를 판별한다."""
    return _REGISTRATION_PATTERN.match(input_str.strip()) is not None


def looks_like_registration_attempt(input_str: str) -> bool:
    """등록 형식과 유사하지만 유효하지 않은 입력인지 판별한다."""
    stripped = input_str.strip()
    if is_registration_input(stripped):
        return False
    return _REGISTRATION_LIKE_PATTERN.search(stripped) is not None


def parse_registration(input_str: str) -> MetersPerUnitLengthUnit:
    """등록 문자열을 파싱하여 MetersPerUnitLengthUnit 인스턴스를 생성한다."""
    match = _REGISTRATION_PATTERN.match(input_str.strip())
    if not match:
        raise RegistrationFormatError("Invalid registration format. Use: 1 cubit = 0.4572 meter")

    name, meters_per_unit = match.group(1), float(match.group(2))
    return MetersPerUnitLengthUnit(name, meters_per_unit)
