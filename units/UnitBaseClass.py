from typing import Dict
from abc import ABC, abstractmethod


class UnitInterface(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_operating_conditions() -> Dict[str, float]:
        pass

    @abstractmethod
    def get_reactor_size() -> Dict[str, float]:
        pass

    @abstractmethod
    def get_pressure_drop() -> float:
        pass
