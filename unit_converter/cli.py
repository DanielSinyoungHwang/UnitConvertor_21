"""CLI 진입점 — 입력 수집, 등록·변환·출력 포맷 조립."""

import sys

from unit_converter.app.input_parser import (
    InputFormatError,
    InvalidNumberError,
    NegativeValueError,
    parse_and_validate,
)
from unit_converter.app.output_formatter import FORMATTERS, SUPPORTED_FORMATS
from unit_converter.app.registration_parser import (
    RegistrationFormatError,
    is_registration_input,
    looks_like_registration_attempt,
    parse_registration,
)
from unit_converter.domain.converter import Converter
from unit_converter.domain.exceptions import UnknownUnitError
from unit_converter.domain.unit_registry import UnitRegistry
from unit_converter.infrastructure.config_loader import load_registry

_PROMPT = (
    "Insert value for converting (ex: meter:2.5) "
    "or register unit (ex: 1 cubit = 0.4572 meter): "
)
_REGISTRATION_FORMAT_HINT = "Invalid registration format. Use: 1 cubit = 0.4572 meter"
_USER_ERRORS = (
    InputFormatError,
    InvalidNumberError,
    UnknownUnitError,
    RegistrationFormatError,
)


def _parse_output_format(argv: list[str]) -> str:
    """명령줄 인자에서 --format 값을 추출한다. 없으면 table."""
    args = list(argv)
    if "--format" not in args:
        return "table"

    index = args.index("--format")
    return args[index + 1]


def run(input_str: str, *, output_format: str = "table", registry: UnitRegistry | None = None) -> int:
    """단일 변환 입력을 처리하고 지정 포맷으로 결과를 stdout에 출력한다."""
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
        supported = ", ".join(SUPPORTED_FORMATS)
        print(f"Unsupported format: {output_format}. Supported: {supported}")
        return 1

    print(formatter(unit, value, converter.convert(unit, value)))
    return 0


def main(argv: list[str] | None = None) -> int:
    """대화형 CLI — 등록 입력 감지 후 변환을 실행하고 종료 코드를 반환한다."""
    output_format = _parse_output_format(sys.argv[1:] if argv is None else argv)
    registry = load_registry()

    first_input = input(_PROMPT).strip()
    if looks_like_registration_attempt(first_input):
        print(_REGISTRATION_FORMAT_HINT)
        return 1

    if is_registration_input(first_input):
        try:
            registry.register(parse_registration(first_input))
        except RegistrationFormatError as exc:
            print(str(exc))
            return 1
        first_input = input(_PROMPT)

    return run(first_input, output_format=output_format, registry=registry)
