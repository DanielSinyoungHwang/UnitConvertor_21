import csv
import io
import json
from collections.abc import Callable

Formatter = Callable[[str, float, dict[str, float]], str]


def format_table(source_unit: str, value: float, results: dict[str, float]) -> str:
    lines = [f"{value} {source_unit} = {converted} {unit}" for unit, converted in results.items()]
    return "\n".join(lines)


def format_json(source_unit: str, value: float, results: dict[str, float]) -> str:
    payload = {
        "source": {"unit": source_unit, "value": value},
        "conversions": [
            {"unit": unit, "value": converted} for unit, converted in results.items()
        ],
    }
    return json.dumps(payload)


def format_csv(source_unit: str, value: float, results: dict[str, float]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["source_unit", "source_value", "target_unit", "target_value"])
    for unit, converted in results.items():
        writer.writerow([source_unit, value, unit, converted])
    return buffer.getvalue().strip()


FORMATTERS: dict[str, Formatter] = {
    "table": format_table,
    "json": format_json,
    "csv": format_csv,
}
