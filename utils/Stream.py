from typing import Dict
from units.UnitBaseClass import UnitInterface


class Stream:
    def __init__(
        self,
        stream_number: int,
        origin: str,
        destination: str,
        U_concentration: float,
        volume: float,
        recycle: bool = False,
    ) -> None:
        self.stream_number = stream_number
        self.origin = origin
        self.destination = destination
        
        
        
        self.U_concentration = U_concentration
        self.volume = volume
        self.recycle = recycle

    def flow_dicts(self) -> Dict[str, float]:
        pass
