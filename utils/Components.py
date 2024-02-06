class Component:
    """
    mol_flow in mol/h
    mass_flow in kg/hr
    vol_flow in m^3/hr
    """

    def __init__(
        self,
        name: str,
        molecular_weight: float,
        flow_rate: float,
        flow_type: str,
        has_volume: bool,
        density: float,
    ):
        self.name = name
        self.molecular_weight = molecular_weight
        self.has_volume = has_volume
        self.density = density

        if has_volume and density is None:
            raise ValueError(
                f"Error in Component {name}: If has_volume is True, density cannot be None"
            )

        if not has_volume and density is not None:
            raise ValueError(
                f"Error in Component {name}: If has_volume is False, density must be None"
            )

        self.update_flow(flow_rate, flow_type)

    def update_flow(self, new_flow_rate, flow_type="mass"):
        """
        Update the component's flow rate.

        Parameters:
        new_flow_rate : float
            The new flow rate value.
        flow_type : str
            The type of the flow rate ('mass', 'molar', or 'volume').
        """
        if flow_type == "mass":
            self.set_mass_flow(new_flow_rate)
        elif flow_type == "molar":
            self.set_molar_flow(new_flow_rate)
        elif flow_type == "volume":
            if not self.has_volume:
                raise ValueError(
                    f"Error in Component {self.name}: Volume flow cannot be set for a component without volume"
                )
            self.set_volume_flow(new_flow_rate)
        else:
            raise ValueError("Invalid flow_type. Must be 'mass', 'molar', or 'volume'")

    def set_mass_flow(self, mass_flow):
        self.mass_flow = mass_flow
        self.mol_flow = (mass_flow / self.molecular_weight) * 1000
        self.vol_flow = 0 if not self.has_volume else mass_flow / self.density

    def set_molar_flow(self, molar_flow):
        self.mol_flow = molar_flow
        self.mass_flow = molar_flow * self.molecular_weight / 1000
        self.vol_flow = 0 if not self.has_volume else self.mass_flow / self.density

    def set_volume_flow(self, volume_flow):
        if not self.has_volume:
            raise ValueError(
                f"Error in Component {self.name}: Cannot set volume flow for a component without volume"
            )
        self.vol_flow = volume_flow
        self.mass_flow = volume_flow * self.density
        self.mol_flow = (self.mass_flow / self.molecular_weight) * 1000

    def __repr__(self) -> str:
        return (
            f"Component {self.name}\n\tMass Flow: {self.mass_flow} kg/h\n\t"
            f"Molar Flow: {self.mol_flow} mol/h\n\t"
            f"Volumetric Flow: {self.vol_flow} m^3/h"
        )


class Water(Component):
    MOLECULAR_WEIGHT = 18.015  # g/mol
    DENSITY = 1000  # kg/m^3

    def __init__(self, flow_rate, flow_type="mass"):
        super().__init__(
            name="Water",
            molecular_weight=Water.MOLECULAR_WEIGHT,
            flow_rate=flow_rate,
            flow_type=flow_type,
            has_volume=True,
            density=Water.DENSITY,
        )


class H2SO4(Component):
    MOLECULAR_WEIGHT = 98.079  # g/mol
    DENSITY = 1830  # kg/m^3

    def __init__(self, flow_rate, flow_type="mass"):
        super().__init__(
            name="H2SO4",
            molecular_weight=H2SO4.MOLECULAR_WEIGHT,
            flow_rate=flow_rate,
            flow_type=flow_type,
            has_volume=True,
            density=H2SO4.DENSITY,
        )


class Cyanex923(Component):
    # https://www.biosynth.com/p/FC168194/100786-00-3-cyanex-923
    MOLECULAR_WEIGHT = 689.11  # g/mol
    DENSITY = 880  # kg/m^3

    def __init__(self, flow_rate, flow_type="mass"):
        super().__init__(
            name="Cyanex923",
            molecular_weight=Cyanex923.MOLECULAR_WEIGHT,
            flow_rate=flow_rate,
            flow_type=flow_type,
            has_volume=True,
            density=Cyanex923.DENSITY,
        )


class Isodecanol(Component):
    # https://pubchem.ncbi.nlm.nih.gov/compound/Isodecanol#section=Density
    MOLECULAR_WEIGHT = 158.28  # g/mol
    DENSITY = 840  # kg/m^3

    def __init__(self, flow_rate, flow_type="mass"):
        super().__init__(
            name="Isodecanol",
            molecular_weight=Isodecanol.MOLECULAR_WEIGHT,
            flow_rate=flow_rate,
            flow_type=flow_type,
            has_volume=True,
            density=Isodecanol.DENSITY,
        )


class ShellSolD70(Component):
    MOLECULAR_WEIGHT = 174  # g/mol
    DENSITY = 796  # kg/m^3

    def __init__(self, flow_rate, flow_type="mass"):
        super().__init__(
            name="ShellSolD70",
            molecular_weight=ShellSolD70.MOLECULAR_WEIGHT,
            flow_rate=flow_rate,
            flow_type=flow_type,
            has_volume=True,
            density=ShellSolD70.DENSITY,
        )


class UO2_2p(Component):
    MOLECULAR_WEIGHT = 270.03  # g/mol
    DENSITY = None

    def __init__(self, flow_rate, flow_type="mass"):
        super().__init__(
            name="UO2_2p",
            molecular_weight=UO2_2p.MOLECULAR_WEIGHT,
            flow_rate=flow_rate,
            flow_type=flow_type,
            has_volume=False,
            density=UO2_2p.DENSITY,
        )


class H2SO5(Component):
    MOLECULAR_WEIGHT = 114.078
    DENSITY = None

    def __init__(self, flow_rate, flow_type="mass"):
        super().__init__(
            name="H2SO5",
            molecular_weight=H2SO5.MOLECULAR_WEIGHT,
            flow_rate=flow_rate,
            flow_type=flow_type,
            has_volume=True,
            density=H2SO5.DENSITY,
        )


class SO4_2m(Component):
    MOLECULAR_WEIGHT = 96.06
    DENSITY = None

    def __init__(self, flow_rate, flow_type="mass"):
        super().__init__(
            name="SO4(2-)",
            molecular_weight=SO4_2m.MOLECULAR_WEIGHT,
            flow_rate=flow_rate,
            flow_type=flow_type,
            has_volume=False,
            density=SO4_2m.DENSITY,
        )


class H_1p(Component):
    MOLECULAR_WEIGHT = 1.01
    DENSITY = None

    def __init__(self, flow_rate, flow_type="mass"):
        super().__init__(
            name="H(+)",
            molecular_weight=H_1p.MOLECULAR_WEIGHT,
            flow_rate=flow_rate,
            flow_type=flow_type,
            has_volume=False,
            density=H_1p.DENSITY,
        )


class Mg(Component):
    MOLECULAR_WEIGHT = 24.305
    DENSITY = None

    def __init__(self, flow_rate, flow_type="mass"):
        super().__init__(
            name="Mg",
            molecular_weight=Mg.MOLECULAR_WEIGHT,
            flow_rate=flow_rate,
            flow_type=flow_type,
            has_volume=False,
            density=Mg.DENSITY,
        )


class Fe(Component):
    MOLECULAR_WEIGHT = 55.845
    DENSITY = None

    def __init__(self, flow_rate, flow_type="mass"):
        super().__init__(
            name="Fe",
            molecular_weight=Fe.MOLECULAR_WEIGHT,
            flow_rate=flow_rate,
            flow_type=flow_type,
            has_volume=False,
            density=Fe.DENSITY,
        )


class SiO2(Component):
    MOLECULAR_WEIGHT = 60.08
    DENSITY = None

    def __init__(self, flow_rate, flow_type="mass"):
        super().__init__(
            name="SiO2",
            molecular_weight=SiO2.MOLECULAR_WEIGHT,
            flow_rate=flow_rate,
            flow_type=flow_type,
            has_volume=False,
            density=SiO2.DENSITY,
        )


class Al2SiO5(Component):
    MOLECULAR_WEIGHT = 162.05
    DENSITY = None

    def __init__(self, flow_rate, flow_type="mass"):
        super().__init__(
            name="Al2SiO5",
            molecular_weight=Al2SiO5.MOLECULAR_WEIGHT,
            flow_rate=flow_rate,
            flow_type=flow_type,
            has_volume=False,
            density=Al2SiO5.DENSITY,
        )


class UO2SO4(Component):
    MOLECULAR_WEIGHT = 366.09
    DENSITY = 3280  # kg /m^3

    def __init__(self, flow_rate, flow_type="mass"):
        super().__init__(
            name="UO2SO4",
            molecular_weight=UO2SO4.MOLECULAR_WEIGHT,
            flow_rate=flow_rate,
            flow_type=flow_type,
            has_volume=True,
            density=UO2SO4.DENSITY,
        )


class MN2_1p(Component):
    MOLECULAR_WEIGHT = 109.88  # g/ mol
    DENSITY = None  # kg /m^3

    def __init__(
        self,
        flow_rate: float,
        flow_type: str = "mass",

    ):
        super().__init__(
            name="MN2(+)",
            molecular_weight=MN2_1p.MOLECULAR_WEIGHT,
            flow_rate=flow_rate,
            flow_type=flow_type,
            has_volume=False,
            density=MN2_1p.DENSITY,
        )

class Al_3p(Component):
    MOLECULAR_WEIGHT = 26.98  # g/ mol
    DENSITY = None  # kg /m^3

    def __init__(
        self,
        flow_rate: float,
        flow_type: str = "mass",

    ):
        super().__init__(
            name="Al(3+)",
            molecular_weight=Al_3p.MOLECULAR_WEIGHT,
            flow_rate=flow_rate,
            flow_type=flow_type,
            has_volume=False,
            density=Al_3p.DENSITY,
        )
