from utils.Stream import Stream
from utils.graph_viz import generate_process_graph, draw_process_graph

units = [
    ["WaterLine", "AcidStorage", "RecycledAcid", "Filtration"],
    ["PLSMixer"],
    ["Extraction", "AcidDecontamination"],
    ["AcidDiluter", "Stripping"],
    ["Precipitation"],
]
streams = [
    Stream(1, "Filtration", "PLSMixer"),
    Stream(1, "RecycledAcid", "PLSMixer"),
    Stream(1, "AcidStorage", "PLSMixer"),
    Stream(1, "PLSMixer", "Extraction"),
    Stream(1, "Extraction", "Stripping"),
    Stream(1, "Extraction", "AcidDecontamination"),
    Stream(1, "Stripping", "Extraction"),
    Stream(1, "AcidStorage", "AcidDiluter"),
    Stream(1, "WaterLine", "AcidDiluter"),
    Stream(1, "AcidDiluter", "Stripping"),
    Stream(1, "Stripping", "Precipitation"),
]

G = generate_process_graph(units=units, streams=streams)
draw_process_graph(G=G)
