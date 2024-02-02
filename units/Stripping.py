from typing import Dict
from units.UnitBaseClass import UnitInterface
from units.McCabeThiele import McCabeThiele
from models.IsothermModeling import IsothermModel
from utils.Stream import Stream

from numpy.polynomial import Polynomial


class Stripping(UnitInterface):
    def __init__(
        self,
        name: str,
        isotherm_model: IsothermModel,
        loaded_organic: Stream,  # in
        stripping_agent: Stream,  # in
        stripped_organic: Stream,  # out
        strip_liquor: Stream,  # out
        num_stages: int,
        efficiency: float = 1,
        plot: bool = False,
    ) -> None:
        super().__init__(name)
        self.name = name
        self.__isotherm_model = isotherm_model
        self.__loaded_organic = loaded_organic
        self.__stripping_agent = stripping_agent
        self.__stripped_organic = stripped_organic
        self.__strip_liquor = strip_liquor

        self.__mcct = McCabeThiele(
            self.__isotherm_model,
            operating_line=Polynomial(  # TODO as well
                [
                    -self.__stripped_organic.U_concentration
                    * (self.__loaded_organic.volume / self.__stripping_agent.volume),
                    self.__loaded_organic.volume / self.__stripping_agent.volume,
                ]
            ),
            inlet_Uconcentration=self.__loaded_organic.U_concentration,
            num_stages=num_stages,
            efficiency=efficiency,
            plot=plot,
        )
        # update the outlets
        self.__stripped_organic = self.__mcct.get_bottom_coord()[0]
        self.__strip_liquor = self.__mcct.get_top_coord()[1]

        print("\nAqeous State")
        print(f"Strip Liquor : {self.__mcct.get_top_coord()[1]}")
        print(f"Dilute Acid : {self.__mcct.get_bottom_coord()[1]}")
        print("\nOrganic Stats")
        print(f"Loaded Organic : {self.__mcct.get_bottom_coord()[0]}")
        print(f"Stripped Organic : {self.__mcct.get_top_coord()[0]}")

    def get_operating_conditions() -> Dict[str, float]:
        pass

    def get_pressure_drop() -> float:
        pass

    def get_unit_dimentions() -> Dict[str, float]:
        pass
