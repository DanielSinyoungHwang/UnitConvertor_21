import sys

from unit_converter.app.input_parser import (
    InputFormatError,
    InvalidNumberError,
    NegativeValueError,
    parse_and_validate,
)
from unit_converter.app.output_formatter import FORMATTERS
from unit_converter.app.registration_parser import (
    RegistrationFormatError,
    is_registration_input,
    parse_registration,
)
from unit_converter.domain.converter import Converter
from unit_converter.domain.exceptions import UnknownUnitError
from unit_converter.domain.unit_registry import UnitRegistry
from unit_converter.infrastructure.config_loader import load_registry

_PROMPT = "Insert value for converting (ex: meter:2.5): "
_USER_ERRORS = (
    InputFormatError,
    InvalidNumberError,
    UnknownUnitError,
    RegistrationFormatError,
)


def _parse_output_format(argv: list[str]) -> str:
    args = list(argv)
    if "--format" not in args:
        return "table"

    index = args.index("--format")
    return args[index + 1]


def run(input_str: str, *, output_format: str = "table", registry: UnitRegistry | None = None) -> int:
    registry = registry or load_registry()
    converter = Converter(registry)

    try:
        unit, value = parse_and_validate(input_str, registry)
    except NegativeValueError:
        print("Negative values are not allowed.")
        return 1
    except _USER_ERRORS as exc:
        print(str(exc))
        return 1

    formatter = FORMATTERS.get(output_format)
    if formatter is None:
        print(f"Unsupported format: {output_format}")
        return 1

    print(formatter(unit, value, converter.convert(unit, value)))
    return 0


def main(argv: list[str] | None = None) -> int:
    output_format = _parse_output_format(sys.argv[1:] if argv is None else argv)
    registry = load_registry()

    first_input = input(_PROMPT).strip()
    if is_registration_input(first_input):
        try:
            registry.register(parse_registration(first_input))
        except RegistrationFormatError as exc:
            print(str(exc))
            return 1
        first_input = input(_PROMPT)

    return run(first_input, output_format=output_format, registry=registry)
