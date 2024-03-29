import networkx as nx
import matplotlib.pyplot as plt


def generate_process_graph(units, streams):
    G = nx.MultiDiGraph()

    for partition_index, unit_group in enumerate(units):
        for unit in unit_group:
            G.add_node(unit, partition=partition_index)

    for stream in streams:
        G.add_edge(
            stream.origin, stream.destination, stream_number=stream.stream_number
        )

    return G


def draw_process_graph(G):
    pos = nx.multipartite_layout(G, subset_key="partition")

    plt.figure(figsize=(12, 8), facecolor="white")

    # Draw edges - NetworkX handles multiple edges in MultiDiGraph automatically
    nx.draw_networkx_edges(
        G,
        pos,
        arrowstyle="->",
        arrowsize=20,
        edge_color="black",
        connectionstyle="arc3,rad=0.1",
    )

    # Draw labels with bounding box
    nx.draw_networkx_labels(
        G,
        pos,
        bbox=dict(facecolor="white", edgecolor="black", boxstyle="round,pad=0.3"),
    )

    # Optionally draw edge labels if needed
    # edge_labels = nx.get_edge_attributes(G, 'stream_number')
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.axis("off")
    plt.show()
