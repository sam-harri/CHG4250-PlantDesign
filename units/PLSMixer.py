from typing import Dict

from units.UnitBaseClass import UnitInterface
from utils.Stream import Stream
from utils.Components import H2SO4, Water, UO2_2p, UO2SO4, SO4_2m


class PLSMixer(UnitInterface):
    MOLARITY_98WpW_H2SO4 = 17.987
    DENSITY_98WpW_H2SO4 = 1800.12

    def __init__(
        self,
        name: str,
        pls_stream: Stream,
        acid_stream: Stream,
        acidic_pls: Stream,
        h2so4_molaity_target: float = 5.0,
    ) -> None:
        super().__init__(name)
        self.__pls_stream = pls_stream
        self.__acid_stream = acid_stream
        self.__acidic_pls = acidic_pls
        self.__h2so4_molaity_target = h2so4_molaity_target

        self.__size_acid_stream()
        self.__combine_inlets()

    def __size_acid_stream(self):
        mol_acid_needed = (
            self.__pls_stream.total_volume * 1000 * self.__h2so4_molaity_target
        )  # mol, *1000 for m^3 to L
        mol_acid_extra_L = (
            PLSMixer.MOLARITY_98WpW_H2SO4 - self.__h2so4_molaity_target
        )  # mol / L
        liters_98acid_needed = mol_acid_needed / mol_acid_extra_L
        mass_98acid_needed = liters_98acid_needed * (
            PLSMixer.DENSITY_98WpW_H2SO4 / 1000
        )
        self.__acid_stream.update_components(
            [H2SO4(mass_98acid_needed * 0.98), Water(mass_98acid_needed * 0.02)]
        )

    def __combine_inlets(self):
        combined_components = Stream.combine_streams(
            [self.__acid_stream, self.__pls_stream]
        )

        updated_components = {comp.name: comp for comp in combined_components}

        if not ("UO2_2p" in updated_components and "SO4(-2)" in updated_components):
            raise ValueError("UO2_2p and SO4(-2) not in the PLSMixer component stream")

        uo2_2p_moles = updated_components["UO2_2p"].mol_flow
        so4_2m_moles = updated_components["SO4(-2)"].mol_flow

        if so4_2m_moles >= uo2_2p_moles:
            updated_components["UO2SO4"] = UO2SO4(
                flow_rate=uo2_2p_moles, flow_type="molar"
            )

            updated_components["SO4(-2)"].set_molar_flow(so4_2m_moles - uo2_2p_moles)

            del updated_components["UO2_2p"]
        else:
            # Handle case where there's not enough SO4(-2) to convert all UO2_2p to UO2SO4
            pass

        updated_components_list = list(updated_components.values())

        self.__acidic_pls.update_components(updated_components_list)

    def mass_balance(self) -> str:
        return f"PLSMixer Mass Balance : {self.__acid_stream.total_mass+self.__pls_stream.total_mass-self.__acidic_pls.total_mass}"

    def get_operating_conditions(self) -> Dict[str, float]:
        pass

    def get_pressure_drop(self) -> float:
        pass

    def get_unit_dimentions(self) -> Dict[str, float]:
        pass
