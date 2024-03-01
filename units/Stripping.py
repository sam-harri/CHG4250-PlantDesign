from copy import deepcopy
from typing import Dict
from units.UnitBaseClass import UnitInterface
from units.McCabeThiele import McCabeThiele
from models.IsothermModeling import IsothermModel
from utils.Stream import Stream
from utils.Components import H2SO4, Water, UO2SO4

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
        stripped_org_Uconc: float,
        loaded_org_Uconc: float,
        num_stages: int,
        efficiency: float = 1,
        OA_ratio: float = 3,
        stripping_agent_molarity: float = 0.2,
        plot: bool = False,
    ) -> None:
        super().__init__(name)
        self.name = name
        self.__isotherm_model = isotherm_model
        self.__loaded_organic = loaded_organic
        self.__stripping_agent = stripping_agent
        self.__stripped_organic = stripped_organic
        self.__strip_liquor = strip_liquor
        self.__stripped_org_Uconc = stripped_org_Uconc
        self.__loaded_org_Uconc = loaded_org_Uconc
        self.__num_stages = num_stages
        self.__efficiency = efficiency
        self.__OA_ratio = OA_ratio
        self.__stripping_agent_molarity = stripping_agent_molarity
        self.__plot = plot
        self.__error = False

        self.__size_stripping_agent()
        self.__built_mcct()
        self.__size_strip_liquor()

    def __size_stripping_agent(self) -> None:
        h2so4_vol_percent = self.__stripping_agent_molarity * (
            H2SO4.MOLECULAR_WEIGHT / H2SO4.DENSITY
        )
        water_vol_percent = 1 - h2so4_vol_percent
        strip_volume = self.__loaded_organic.total_volume / self.__OA_ratio
        self.__stripping_agent.update_components(
            [
                Water(strip_volume * water_vol_percent, "volume"),
                H2SO4(strip_volume * h2so4_vol_percent, "volume"),
            ]
        )
        # print(
        #     f'checking molarity SA : {self.__stripping_agent.get_component_property("H2SO4", "molar_flow")/(self.__stripping_agent.total_volume*1000)}'
        # )
        # print(
        #     f"checking volume : {self.__stripping_agent.total_volume/self.__loaded_organic.total_volume}"
        # )

    def __built_mcct(self) -> None:
        self.__mcct = McCabeThiele(
            self.__isotherm_model,
            operating_line=Polynomial(
                [
                    -(self.__OA_ratio * self.__stripped_org_Uconc),  # b
                    self.__OA_ratio,  # m
                ]
            ),
            inlet_Uconcentration=self.__loaded_org_Uconc,
            num_stages=self.__num_stages,
            efficiency=self.__efficiency,
            plot=self.__plot,
            min=self.__stripped_org_Uconc,
        )
        if self.__mcct.error:
            self.__error = True
            return

        # print("\nAqeous State")
        # print(f"Strip Liquor : {self.__mcct.get_top_coord()[1]}")
        # print(f"Dilute Acid : {self.__mcct.get_bottom_coord()[1]}")
        # print("\nOrganic Stats")
        # print(f"Stripped Orgnic : {self.__mcct.get_bottom_coord()[0]}")
        # print(f"Loaded Organic : {self.__mcct.get_top_coord()[0]}")

    def __size_strip_liquor(self) -> None:
        if self.__error:
            return
        strip_liq_comps = deepcopy(self.__stripping_agent.components)
        uo2so4_mass = self.__loaded_organic.get_component_property(
            "UO2SO4", "mass_flow"
        ) - self.__stripped_organic.get_component_property("UO2SO4", "mass_flow")
        strip_liq_comps.append(UO2SO4(uo2so4_mass, "mass"))
        self.__strip_liquor.update_components(strip_liq_comps)
        self.mass_balance_check()

    def get_strip_concentration(self) -> float:
        return self.__mcct.get_top_coord()[1]

    def error(self):
        return self.__error

    def mass_balance(self) -> str:
        return f"Stripping Mass Balance : {round(self.__loaded_organic.total_mass + self.__stripping_agent.total_mass - self.__stripped_organic.total_mass - self.__strip_liquor.total_mass,4)}"

    def mass_balance_check(self) -> None:
        if (
            round(
                self.__loaded_organic.total_mass
                + self.__stripping_agent.total_mass
                - self.__stripped_organic.total_mass
                - self.__strip_liquor.total_mass,
                4,
            )
            != 0
        ):
            raise ValueError("Failed Mass Balance on Strippping")
    
    def stripping_per_stage(self) -> float:
        return (self.__mcct.get_top_coord()[0] - self.__mcct.get_bottom_coord()[0]) / self.__num_stages

    def get_operating_conditions(self) -> Dict[str, float]:
        pass

    def get_unit_dimentions(self) -> Dict[str, float]:
        pass

    def get_pressure_drop(self) -> float:
        pass
