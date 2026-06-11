def format_table(source_unit: str, value: float, results: dict[str, float]) -> str:
    lines = [f"{value} {source_unit} = {converted} {unit}" for unit, converted in results.items()]
    return "\n".join(lines)
