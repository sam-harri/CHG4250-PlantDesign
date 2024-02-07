from typing import Dict
from abc import ABC, abstractmethod


class UnitInterface(ABC):
    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def get_operating_conditions(self) -> Dict[str, float]:
        pass

    @abstractmethod
    def get_unit_dimentions(self) -> Dict[str, float]:
        pass

    @abstractmethod
    def get_pressure_drop(self) -> float:
        pass

    @abstractmethod
    def mass_balance(self) -> str:
        pass
