from typing import Dict
from units.UnitBaseClass import UnitInterface
from units.McCabeThiele import McCabeThiele
from models.IsothermModeling import IsothermModel
from utils.Stream import Stream

from numpy.polynomial import Polynomial


class Extraction(UnitInterface):
    def __init__(
        self,
        name: str,
        isotherm_model: IsothermModel,
        pls: Stream,  # in
        stripped_organic: Stream,  # in
        loaded_organic: Stream,  # out
        depleted_raffinate: Stream,  # out
        num_stages: int,
        efficiency: float = 1,
        plot: bool = False,
    ) -> None:
        super().__init__(name)
        self.name = name
        self.__isotherm_model = isotherm_model
        self.__pls = pls
        self.__stripped_organic = stripped_organic
        self.__loaded_organic = loaded_organic
        self.__depleted_raffinate = depleted_raffinate

        self.__mcct = McCabeThiele(
            self.__isotherm_model,
            operating_line=Polynomial(  # TODO this
                [
                    self.__stripped_organic.U_concentration,
                    self.__pls.volume / self.__stripped_organic.volume,
                ]
            ),
            inlet_Uconcentration=self.__pls.U_concentration,
            num_stages=num_stages,
            efficiency=efficiency,
            plot=plot,
        )

        # update the outlets
        self.__loaded_organic.U_concentration = self.__mcct.get_top_coord()[1]
        self.__depleted_raffinate.U_concentration = self.__mcct.get_bottom_coord()[0]

        print("\nAqeous Stats")
        print(f"Initial PLS : {self.__mcct.get_top_coord()[0]}")
        print(f"Depleted Raffinate : {self.__mcct.get_bottom_coord()[0]}")
        print("\nOrganic Stats")
        print(f"Stripped Organic : {self.__mcct.get_bottom_coord()[1]}")
        print(f"Loaded Organic : {self.__mcct.get_top_coord()[1]}")

    def get_loaded_organic_Uconcentration(self) -> float:
        return self.__mcct.get_top_coord()[1]

    def get_operating_conditions(self) -> Dict[str, float]:
        pass

    def get_pressure_drop(self) -> float:
        pass

    def get_unit_dimentions(self) -> Dict[str, float]:
        pass
