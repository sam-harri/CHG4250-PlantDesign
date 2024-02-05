from typing import Dict, List
from units.UnitBaseClass import UnitInterface
from units.McCabeThiele import McCabeThiele
from models.IsothermModeling import IsothermModel
from utils.Stream import Stream
from utils.Components import UO2SO4, ShellSolD70, Cyanex923, Isodecanol
from copy import deepcopy

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
        OA_ratio : float = 1.5,
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
        self.__OA_ratio = OA_ratio
        self.__plot = plot
        
        self.__size_organics()
        self.__build_mcct()
        self.__update_outlets()
        
    def __size_organics(self) -> None:
        uo2so4_mass = self.__stripped_organic.get_component_property("UO2SO4", "mass_flow")
        pls_volume = self.__pls.total_volume
        self.__stripped_organic.update_components([
            ShellSolD70(pls_volume * 0.8 * self.__OA_ratio,"volume"),
            Cyanex923(pls_volume * 0.1 * self.__OA_ratio,"volume"),
            Isodecanol(pls_volume * 0.1 * self.__OA_ratio,"volume"),
            UO2SO4(uo2so4_mass, "mass"),
        ])
        
    def __build_mcct(self) -> None:
        stripped_org_Uconc = (self.__stripped_organic.get_component_property("UO2SO4", "mass_flow") * 0.6502) / self.__stripped_organic.total_volume
        pls_Uconc =  (self.__pls.get_component_property("UO2SO4", "mass_flow") * 0.6502) / self.__pls.total_volume
        
        self.__mcct = McCabeThiele(
            self.__isotherm_model,
            operating_line=Polynomial(
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
        
        self.__inital_pls_Uconc = self.__mcct.get_top_coord()[0]
        self.__depleted_raffinate_Uconc = self.__mcct.get_bottom_coord()[0]
        self.__loaded_org_Uconc = self.__mcct.get_top_coord()[1]
        self.__stripped_org_Uconc = self.__mcct.get_bottom_coord()[1]
        print(f"inital_pls_Uconc : {self.__mcct.get_top_coord()[0]}")
        print(f"depleted_raffinate_Uconc : {self.__mcct.get_bottom_coord()[0]}")
        print(f"loaded_org_Uconc : {self.__mcct.get_top_coord()[1]}")
        print(f"stripped_org_Uconc : {self.__mcct.get_bottom_coord()[1]}")
        self.extraction_percent = 1 - (self.__depleted_raffinate_Uconc/self.__inital_pls_Uconc)
    
    def __update_outlets(self) -> None:
        loaded_org_comps = deepcopy(self.__stripped_organic.components)
        uo2so4_mass = (self.__loaded_org_Uconc * self.__stripped_organic.total_volume) / 0.6502
        print(uo2so4_mass)
        
        for c in loaded_org_comps:
            if c.name == "UO2SO4":
                c.update_flow(uo2so4_mass,"mass")
        self.__loaded_organic.update_components(loaded_org_comps)
        
        dr_comps = deepcopy(self.__pls.components)
        uo2so4_mass2 = self.__pls.get_component_property("UO2SO4", "mass_flow") + self.__stripped_organic.get_component_property("UO2SO4", "mass_flow")-uo2so4_mass
        for c in dr_comps:
            if c.name == "UO2SO4":
                c.update_flow(uo2so4_mass2,"mass")
        self.__depleted_raffinate.update_components(dr_comps)
        
    def mass_balance(self) -> str:
        return f"Extraction Mass Balance : {round(self.__pls.total_mass+self.__stripped_organic.total_mass-self.__loaded_organic.total_mass-self.__depleted_raffinate.total_mass,4)}"

    def get_operating_conditions(self) -> Dict[str, float]:
        pass

    def get_pressure_drop(self) -> float:
        pass

    def get_unit_dimentions(self) -> Dict[str, float]:
        pass
