from __future__ import annotations
from typing import List, Dict
from utils.Components import Component


class Stream:
    ATTRIBUTES: Dict[str, int] = {"mass_flow": 0, "molar_flow": 1, "volume_flow": 2}

    def __init__(
        self,
        stream_number: int,
        origin: str,
        destination: str,
        components: List[Component] = [],
        recycle: bool = False,
    ) -> None:
        self.stream_number = stream_number
        self.origin = origin
        self.destination = destination
        self.components: List[Component] = sorted(components, key=lambda x: x.name)
        self.component_indices: Dict[str, int] = {
            component.name: idx for idx, component in enumerate(self.components)
        }
        self.recycle = recycle
        self.total_mass: float = 0.0
        self.total_molar_flow: float = 0.0
        self.total_volume: float = 0.0
        self._update_totals_and_state_vector()

    def _create_state_vector(self) -> List[List[float]]:
        return [
            [component.mass_flow, component.mol_flow, component.vol_flow]
            for component in self.components
        ]

    def _update_totals_and_state_vector(self) -> None:
        """Recalculate total mass, molar flow, and volume, and update the state vector."""
        self.total_mass = sum(component.mass_flow for component in self.components)
        self.total_molar_flow = sum(component.mol_flow for component in self.components)
        self.total_volume = sum(
            component.vol_flow for component in self.components if component.has_volume
        )
        self.state_vector = self._create_state_vector()
        self.density = (
            self.total_mass / self.total_volume if self.total_volume != 0 else None
        )

    def update_components(self, new_components: List[Component]) -> None:
        self.components = sorted(new_components, key=lambda x: x.name)
        self.component_indices = {
            component.name: idx for idx, component in enumerate(self.components)
        }
        self._update_totals_and_state_vector()

    def get_component_property(self, component_name: str, property_name: str) -> float:
        """mass_flow, molar_flow, volume_flow, mass_fraction, molar_fraction"""
        if component_name not in self.component_indices.keys():
            raise ValueError(
                f"Component {component_name} not found in stream {self.stream_number}"
            )

        component_idx = self.component_indices[component_name]
        component = self.components[component_idx]

        if property_name == "mass_flow":
            return component.mass_flow
        elif property_name == "molar_flow":
            return component.mol_flow
        elif property_name == "volume_flow":
            return component.vol_flow
        elif property_name == "mass_fraction":
            return component.mass_flow / self.total_mass if self.total_mass > 0 else 0
        elif property_name == "molar_fraction":
            return (
                component.mol_flow / self.total_molar_flow
                if self.total_molar_flow > 0
                else 0
            )
        elif property_name == "volume_fraction":
            return (
                component.vol_flow / self.total_volume
                if self.total_volume > 0 and component.has_volume
                else 0
            )
        else:
            raise ValueError(f"Property {property_name} not a valid query")

    @staticmethod
    def combine_streams(streams: List[Stream]) -> List[Component]:
        combined_data = {}

        for stream in streams:
            for component in stream.components:
                if component.name not in combined_data:
                    combined_data[component.name] = {
                        "total_mass": 0,
                        "class": type(
                            component
                        ),  # Store the class of the component for instantiation
                    }
                combined_data[component.name]["total_mass"] += component.mass_flow

        # Creating new component instances with combined mass flows
        combined_components = []
        for name, data in combined_data.items():
            # Instantiate the correct component class with combined mass flow
            combined_components.append(
                data["class"](flow_rate=data["total_mass"], flow_type="mass")
            )

        return combined_components

    def __repr__(self) -> str:
        component_details: str = "\n".join(
            [
                f"{idx}: {comp.name} - Mass flow: {vec[0]:.6f} kg/h, "
                f"Molar flow: {vec[1]:.6f} mol/h, Volume flow: {vec[2]:.6f} m^3/h"
                for idx, (comp, vec) in enumerate(
                    zip(self.components, self.state_vector)
                )
            ]
        )
        return f"Stream {self.stream_number} from {self.origin} to {self.destination}:\n{component_details}"
