from typing import Dict
from units.UnitBaseClass import UnitInterface

class Stream():
    def __init__(self, stream_number : int, origin : UnitInterface, target : UnitInterface) -> None:
        self.stream_number = stream_number
        self.origin = origin
        self.target = target
    
    def flow_dicts(self) -> Dict[str, float]:
        pass