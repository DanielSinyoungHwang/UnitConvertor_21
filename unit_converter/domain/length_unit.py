"""길이 단위 인터페이스 및 meter 기준 비율 구현체."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class LengthUnit(Protocol):
    """길이 단위의 공통 계약 — 이름과 meter ↔ 단위 변환."""

    @property
    def name(self) -> str:
        """단위 식별자 (예: meter, feet)."""
        ...

    def to_meter(self, value: float) -> float:
        """단위 값을 meter로 변환한다."""
        ...

    def from_meter(self, meters: float) -> float:
        """meter 값을 이 단위로 변환한다."""
        ...


class MetersPerUnitLengthUnit:
    """1 unit = meters_per_unit meter 비율로 정의된 길이 단위."""

    def __init__(self, name: str, meters_per_unit: float) -> None:
        """단위 이름과 1단위당 meter 비율을 설정한다."""
        self._name = name
        self._meters_per_unit = meters_per_unit

    @property
    def name(self) -> str:
        """등록·조회에 사용되는 단위 이름."""
        return self._name

    def to_meter(self, value: float) -> float:
        """value × meters_per_unit으로 meter 값을 계산한다."""
        return value * self._meters_per_unit

    def from_meter(self, meters: float) -> float:
        """meter ÷ meters_per_unit으로 이 단위 값을 계산한다."""
        return meters / self._meters_per_unit
