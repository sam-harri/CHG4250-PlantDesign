from models.IsothermModeling import IsothermModel
from units.Extraction import Extraction
from units.Stripping import Stripping
from utils.Stream import Stream
from utils.graph_viz import generate_process_graph, draw_process_graph

import networkx as nx
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # stream definitions
    pls = Stream(
        stream_number=1,
        origin="Filtration",
        destination="Extraction",
        U_concentration=15.5,
        volume=2,
    )

    stripped_organic = Stream(
        stream_number=2,
        origin="Stripping",
        destination="Extraction",
        U_concentration=0.5,
        volume=3,
    )

    loaded_organic = Stream(
        stream_number=3,
        origin="Extraction",
        destination="Stripping",
        U_concentration=None,
        volume=3,
    )

    stripping_agent = Stream(
        stream_number=4,
        origin="DiluteAcidFeed",
        destination="Stripping",
        U_concentration=0,
        volume=1,
    )

    depleted_raffinate = Stream(
        stream_number=5,
        origin="Extraction",
        destination="AcidDecontamination",
        U_concentration=None,
        volume=2,
    )

    strip_liquor = Stream(
        stream_number=6,
        origin="Stripping",
        destination="Precipitation",
        U_concentration=None,
        volume=1,
    )

    extraction_isotherm = IsothermModel(
        data_path="data/UeqExtrationData.csv",
        x_label="U(aq)",
        y_label="U(org)",
    )

    stripping_isotherm = IsothermModel(
        data_path="data/UeqStrippingData.csv",
        x_label="U(org)",
        y_label="U(aq)",
    )

    extraction_unit = Extraction(
        name="Extraction",
        isotherm_model=extraction_isotherm,
        pls=pls,
        stripped_organic=stripped_organic,
        loaded_organic=loaded_organic,
        depleted_raffinate=depleted_raffinate,
        num_stages=5,
        efficiency=0.9,
        plot=True,
    )

    stripping_unit = Stripping(
        name="Stripping",
        isotherm_model=stripping_isotherm,
        loaded_organic=loaded_organic,
        stripping_agent=stripping_agent,
        stripped_organic=stripped_organic,
        strip_liquor=strip_liquor,
        num_stages=4,
        efficiency=0.9,
        plot=True,
    )
    
    units = [
        ["Filtration"],
        ["AcidDecontamination", "Extraction"],
        ["Stripping", "DiluteAcidFeed"],
        ["Precipitation"],
    ]
    
    streams = [
        pls,
        stripped_organic,
        loaded_organic,
        stripping_agent,
        depleted_raffinate,
        strip_liquor,
    ]
    
    
    G = generate_process_graph(units=units, streams=streams)
    draw_process_graph(G=G)
    
    A = nx.adjacency_matrix(G=G)
    print(A.todense())
