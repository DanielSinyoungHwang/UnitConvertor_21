import sys

from unit_converter.app.input_parser import (
    InputFormatError,
    InvalidNumberError,
    NegativeValueError,
    parse_and_validate,
)
from unit_converter.app.output_formatter import format_table
from unit_converter.domain.converter import Converter
from unit_converter.domain.exceptions import UnknownUnitError
from unit_converter.domain.unit_registry import UnitRegistry


def _print_error(message: str) -> None:
    print(message)


def run(input_str: str, *, output_format: str = "table") -> int:
    registry = UnitRegistry()
    converter = Converter(registry)

    try:
        unit, value = parse_and_validate(input_str, registry)
    except InputFormatError as exc:
        _print_error(str(exc))
        return 1
    except InvalidNumberError as exc:
        _print_error(str(exc))
        return 1
    except NegativeValueError:
        _print_error("Negative values are not allowed.")
        return 1
    except UnknownUnitError as exc:
        _print_error(str(exc))
        return 1

    results = converter.convert(unit, value)

    if output_format == "table":
        print(format_table(unit, value, results))
    else:
        _print_error(f"Unsupported format: {output_format}")
        return 1

    return 0


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    output_format = "table"
    if "--format" in args:
        index = args.index("--format")
        output_format = args[index + 1]
        del args[index : index + 2]

    input_str = input("Insert value for converting (ex: meter:2.5): ")
    return run(input_str, output_format=output_format)
