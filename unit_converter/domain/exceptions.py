class UnknownUnitError(Exception):
    def __init__(self, unit: str) -> None:
        self.unit = unit
        super().__init__(f"Unknown unit: {unit}")
