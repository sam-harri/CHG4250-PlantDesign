from typing import Dict
from units.UnitBaseClass import UnitInterface
from units.McCabeThiele import McCabeThiele
from models.IsothermModeling import IsothermModel

from numpy.polynomial import Polynomial


class Stripping(UnitInterface):
    def __init__(
        self,
        name : str,
        isotherm_model: IsothermModel,
        operating_line: Polynomial,
        inlet_Uconcentration: float,
        num_stages: int,
        efficiency: float = 1,
        plot: bool = False,
    ) -> None:
        super().__init__()
        self.__isotherm_model = isotherm_model
        self.__mcct = McCabeThiele(
            self.__isotherm_model,
            operating_line=operating_line,
            inlet_Uconcentration=inlet_Uconcentration,
            num_stages=num_stages,
            efficiency=efficiency,
            plot=plot,
        )

    def get_operating_conditions() -> Dict[str, float]:
        pass

    def get_pressure_drop() -> float:
        pass

    def get_reactor_size() -> Dict[str, float]:
        pass
