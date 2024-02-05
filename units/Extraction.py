from typing import Dict, List
from units.UnitBaseClass import UnitInterface
from units.McCabeThiele import McCabeThiele
from models.IsothermModeling import IsothermModel
from utils.Stream import Stream
from utils.Components import UO2SO4, ShellSolD70, Cyanex923, Isodecanol

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
        self.__num_stages  = num_stages
        self.__efficiency = efficiency
        self.__plot = plot
        
        self.__size_organics()
        self.__build_mcct()
        
    def __size_organics(self) -> None:
        uo2so4_mass = self.__stripped_organic.get_component_property("UO2SO4", "mass_flow")
        pls_volume = self.__pls.total_volume
        self.__stripped_organic.update_components([
            ShellSolD70(pls_volume * 0.8,"volume"),
            Cyanex923(pls_volume * 0.1,"volume"),
            Isodecanol(pls_volume * 0.1,"volume"),
            UO2SO4(uo2so4_mass, "mass"),
        ])
        
    def __build_mcct(self) -> None:
        stripped_org_Uconc = (self.__stripped_organic.get_component_property("UO2SO4", "mass_flow") * 0.6502) / self.__stripped_organic.total_volume
        pls_Uconc =  (self.__pls.get_component_property("UO2SO4", "mass_flow") * 0.6502) / self.__pls.total_volume
        
        print()
        
        self.__mcct = McCabeThiele(
            self.__isotherm_model,
            operating_line=Polynomial(  # TODO this
                [
                    stripped_org_Uconc,
                    self.__pls.total_volume / self.__stripped_organic.total_volume,
                ]
            ),
            inlet_Uconcentration=pls_Uconc,
            num_stages=self.__num_stages,
            efficiency=self.__efficiency,
            plot=self.__plot,
        )

        # update the outlets
        # self.__loaded_organic.U_concentration = self.__mcct.get_top_coord()[1]
        # self.__depleted_raffinate.U_concentration = self.__mcct.get_bottom_coord()[0]

        print("\nAqeous Stats")
        print(f"Initial PLS : {self.__mcct.get_top_coord()[0]}")
        print(f"Depleted Raffinate : {self.__mcct.get_bottom_coord()[0]}")
        print("\nOrganic Stats")
        print(f"Stripped Organic : {self.__mcct.get_bottom_coord()[1]}")
        print(f"Loaded Organic : {self.__mcct.get_top_coord()[1]}")

    def get_loaded_organic_Uconcentration(self) -> float:
        return self.__mcct.get_top_coord()[1]
    
    def mass_balance(self) -> str:
        return f"Extraction Mass Balance : {self.__pls.total_mass+self.__stripped_organic.total_mass-self.__loaded_organic.total_mass-self.__depleted_raffinate.total_mass}"

    def get_operating_conditions(self) -> Dict[str, float]:
        pass

    def get_pressure_drop(self) -> float:
        pass

    def get_reactor_size(self) -> Dict[str, float]:
        pass
