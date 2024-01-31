from typing import Dict, List
from abc import ABC, abstractmethod


class UnitInterface(ABC):
    def __init__(self) -> None:
    # def __init__(self, name : str, inlet_streams : List, outlet_streams : List) -> None:
        # self.name = name
        # self.inlet_streams = inlet_streams
        # self.outlet_streams = outlet_streams
        pass

    @abstractmethod
    def get_operating_conditions(self) -> Dict[str, float]:
        pass

    @abstractmethod
    def get_reactor_size(self) -> Dict[str, float]:
        pass

    @abstractmethod
    def get_pressure_drop(self) -> float:
        pass
