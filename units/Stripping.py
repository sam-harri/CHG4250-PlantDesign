from typing import Dict, List
from units.UnitBaseClass import UnitInterface
from units.McCabeThiele import McCabeThiele
from models.IsothermModeling import IsothermModel
from utils.Stream import Stream

from numpy.polynomial import Polynomial


class Stripping(UnitInterface):
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
        self.__loadedO = [x for x in inlet_streams if x.origin == "Extraction"][0] # O
        self.__stripping_agent = [x for x in inlet_streams if x.origin == "Diluted Acid"][0] # A
        
        self.__mcct = McCabeThiele(
            self.__isotherm_model,
            operating_line=Polynomial([0, self.__loadedO.volume / self.__stripping_agent.volume]),
            inlet_Uconcentration=self.__loadedO.U_concentration,
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
