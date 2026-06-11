"""변환 결과를 table / json / csv 형식으로 직렬화."""

import csv
import io
import json
from collections.abc import Callable

Formatter = Callable[[str, float, dict[str, float]], str]


def format_table(source_unit: str, value: float, results: dict[str, float]) -> str:
    """변환 결과를 사람이 읽기 쉬운 줄 단위 텍스트로 출력한다."""
    lines = [f"{value} {source_unit} = {converted} {unit}" for unit, converted in results.items()]
    return "\n".join(lines)


def format_json(source_unit: str, value: float, results: dict[str, float]) -> str:
    """변환 결과를 JSON 객체 문자열로 직렬화한다."""
    payload = {
        "source": {"unit": source_unit, "value": value},
        "conversions": [
            {"unit": unit, "value": converted} for unit, converted in results.items()
        ],
    }
    return json.dumps(payload)


def format_csv(source_unit: str, value: float, results: dict[str, float]) -> str:
    """변환 결과를 CSV(헤더 + 행) 문자열로 직렬화한다."""
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["source_unit", "source_value", "target_unit", "target_value"])
    for unit, converted in results.items():
        writer.writerow([source_unit, value, unit, converted])
    return buffer.getvalue().strip()


# CLI --format 옵션과 포맷터 함수 매핑
SUPPORTED_FORMATS = ("csv", "json", "table")

FORMATTERS: dict[str, Formatter] = {
    "table": format_table,
    "json": format_json,
    "csv": format_csv,
}
