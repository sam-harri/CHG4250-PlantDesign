from typing import Dict, List
from units.UnitBaseClass import UnitInterface
from units.McCabeThiele import McCabeThiele
from models.IsothermModeling import IsothermModel
from utils.Stream import Stream

from numpy.polynomial import Polynomial


class Extraction(UnitInterface):
    def __init__(
        self,
        name : str,
        isotherm_model: IsothermModel,
        inlet_streams : List[Stream],
        outlet_streams : List[Stream],
        num_stages: int,
        efficiency: float = 1,
        plot: bool = False,
    ) -> None:
        super().__init__()
        self.__isotherm_model = isotherm_model
        self.__pls = [x for x in inlet_streams if x.origin == "Filtration"][0] # A
        self.__barrenO = [x for x in inlet_streams if x.origin == "Stripping"][0] # O
        
        self.__mcct = McCabeThiele(
            self.__isotherm_model,
            operating_line=Polynomial([self.__barrenO.U_concentration, self.__pls.volume / self.__barrenO.volume]),
            inlet_Uconcentration=self.__pls.U_concentration,
            num_stages=num_stages,
            efficiency=efficiency,
            plot=plot,
        )

    def get_loaded_organic_Uconcentration(self) -> float:
        return self.__mcct.get_loaded_organic()

    def get_operating_conditions(self) -> Dict[str, float]:
        pass

    def get_pressure_drop(self) -> float:
        pass

    def get_reactor_size(self) -> Dict[str, float]:
        pass
