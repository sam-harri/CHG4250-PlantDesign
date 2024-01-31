from typing import Dict
from units.UnitBaseClass import UnitInterface
from units.McCabeThiele import McCabeThiele
from models.IsothermModeling import IsothermModel


class Extraction(UnitInterface):
    def __init__(
        self,
        isotherm_model: IsothermModel,
        ratio: float,
        inlet_Uconcentration: float,
        num_stages: int,
        efficiency: float = 1,
        plot: bool = False,
    ) -> None:
        super().__init__()
        self.__isotherm_model = isotherm_model
        self.__mcct = McCabeThiele(
            self.__isotherm_model,
            ratio=ratio,
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