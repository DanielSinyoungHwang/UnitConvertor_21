import re

from unit_converter.domain.length_unit import MetersPerUnitLengthUnit

_REGISTRATION_PATTERN = re.compile(
    r"^\s*1\s+(\w+)\s*=\s*([0-9.]+)\s+meter\s*$",
    re.IGNORECASE,
)


class RegistrationFormatError(Exception):
    pass


def parse_registration(input_str: str) -> MetersPerUnitLengthUnit:
    match = _REGISTRATION_PATTERN.match(input_str.strip())
    if not match:
        raise RegistrationFormatError("Invalid registration format. Use: 1 cubit = 0.4572 meter")

    name, meters_per_unit = match.group(1), float(match.group(2))
    return MetersPerUnitLengthUnit(name, meters_per_unit)
