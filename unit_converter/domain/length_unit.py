from typing import Protocol, runtime_checkable


@runtime_checkable
class LengthUnit(Protocol):
    @property
    def name(self) -> str: ...

    def to_meter(self, value: float) -> float: ...

    def from_meter(self, meters: float) -> float: ...


class MetersPerUnitLengthUnit:
    """1 unit = meters_per_unit meter."""

    def __init__(self, name: str, meters_per_unit: float) -> None:
        self._name = name
        self._meters_per_unit = meters_per_unit

    @property
    def name(self) -> str:
        return self._name

    def to_meter(self, value: float) -> float:
        return value * self._meters_per_unit

    def from_meter(self, meters: float) -> float:
        return meters / self._meters_per_unit
