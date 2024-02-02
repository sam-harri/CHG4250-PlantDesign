from utils.Components import *
from utils.Stream import Stream

water = Water(flow_rate=1000, flow_type="mass")
isodecanol = Isodecanol(flow_rate=200, flow_type="mass")
shellsold70 = ShellSolD70(flow_rate=300, flow_type="mass")

stream1 = Stream(1, "Reactor", "Separator", [water, isodecanol, shellsold70])
print(stream1)

new_water = Water(flow_rate=1500, flow_type="mass")
stream1.update_components([new_water, isodecanol, shellsold70])
print("\nAfter update:")
print(stream1)

print(stream1.get_component_property("Water", "mass_flow"))