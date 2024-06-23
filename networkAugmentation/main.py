import sys

import networkx as nx
import numpy as np
from networkx import resistance_distance


def kirchhoff_index(graph):
    #################################################
    # Obtain Kirchhof index
    #################################################
    n = len(graph.nodes)
    Kf = 0
    for u in range(n):
        for v in range(u + 1, n):
            Kf += resistance_distance(graph, list(graph.nodes)[u], list(graph.nodes)[v])
    return Kf


def calculations(graph, writer):
    #################################################
    # Calculate diameter
    #################################################
    dm = nx.diameter(graph)
    writer.write(f"Diameter of the graph: {dm}\n")

    #################################################
    # Calculate algebraic connectivity
    #################################################
    a_connectivity = nx.algebraic_connectivity(graph)
    writer.write(f"Algebraic connectivity of the graph: {a_connectivity}\n")

    #################################################
    # Calculate average shortest path length
    #################################################
    path_len = nx.average_shortest_path_length(graph)
    writer.write(f"Average shortest path length of the graph: {path_len}\n")

    #################################################
    # Calculate Kirchhoff index
    #################################################
    kf_index = kirchhoff_index(graph)
    writer.write(f"Kirchhoff index of the graph: {kf_index}\n")

    #################################################
    # Calculate number of spanning trees
    #################################################
    eigenvalues = nx.linalg.spectrum.laplacian_spectrum(graph)
    sorted_eigenvalues = np.sort(eigenvalues)[::-1]
    num_spanning_trees = np.prod(sorted_eigenvalues[:-1]) / len(sorted_eigenvalues)
    formatted_num_spanning_trees = '{:.6f}'.format(num_spanning_trees)
    writer.write(f"Number of Spanning Trees: {formatted_num_spanning_trees}\n")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python Main.py <file_name>")
        sys.exit(1)

    read_path = sys.argv[1]
    write_path = sys.argv[2]

    G = nx.read_pajek(read_path, encoding='UTF-8')
    G1 = nx.Graph(G)

    #################################################
    # List of edges to add to the Ibiza graph
    #################################################
    ibiza_list=[("15", "16"), ("9", "16"), ("9", "14"), ("9", "11"), ("13", "14"), ("4", "13"), ("5", "11"),
                ("4", "22"), ("5", "22"), ("21", "24"), ("2", "5"), ("3", "5")]

    #################################################
    # List of edges to add to the Menorca graph
    #################################################
    menorca_list=[("Son Seu", "Naveta des Tudons"), ("Cala d'Artrutx", "Santa Galdana"), ("Ciutadella", "Santa Galdana"),
    ("Naveta des Tudons", "Santa Galdana"), ("Santa Galdana", "Sant Tomas"), ("Sant Tomas", "Platja de son Bou"), ("Son Bou", "Cala en Porter"),
    ("Alaior", "Binifamis"), ("Alaior", "Estancia de ses Penyes"), ("Sant Climent", "Sant Lluis")]

    edge_list=[]
    if(read_path.endswith("ibiza.net")):
        edge_list=ibiza_list
    elif(read_path.endswith("menorca.net")):
        edge_list=menorca_list

    with open(write_path, 'w') as writer:

        writer.write("Original graph:\n")
        calculations(G1, writer)
        writer.write("\n")

        for edge in edge_list:
            #################################################
            # G_temp is used so that the new edge only exists during current iteration
            #################################################
            G_temp = G1.copy()
            G_temp.add_edge(*edge)
            writer.write(f"Adding edge {edge}:\n")
            calculations(G_temp, writer)
            writer.write("\n")