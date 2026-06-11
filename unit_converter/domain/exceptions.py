"""도메인 계층 예외 정의."""


class UnknownUnitError(Exception):
    """레지스트리에 없는 단위 이름으로 조회할 때 발생."""

    def __init__(self, unit: str) -> None:
        """미등록 단위 이름을 예외 메시지에 포함한다."""
        self.unit = unit
        super().__init__(
            f"Unknown unit: {unit}. To register: 1 {unit} = <ratio> meter"
        )
