from typing import Dict, List
from abc import ABC, abstractmethod


class UnitInterface(ABC):
    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def get_operating_conditions(self) -> Dict[str, float]:
        pass

    @abstractmethod
    def get_reactor_size(self) -> Dict[str, float]:
        pass

    @abstractmethod
    def get_pressure_drop(self) -> float:
        pass
