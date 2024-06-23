import networkx as nx
import numpy as np
from networkx import resistance_distance, diameter, algebraic_connectivity

def kirchhoff_index(G1):
    #################################################
    # Obtain Kirchhof index
    #################################################
    n = len(G1.nodes)
    Kf = 0
    for u in range(n):
        for v in range(u + 1, n):
            Kf += resistance_distance(G1, list(G1.nodes)[u], list(G1.nodes)[v])
    return Kf

def calculations(G1):
    #################################################
    # Print diameter
    #################################################
    dm = diameter(G1)
    print("Diameter of the graph:", dm)

    #################################################
    # Print edge connectivity
    #################################################
    e_connectivity = nx.algorithms.connectivity.edge_connectivity(G1)
    print("Edge connectivity of the graph:", e_connectivity)

    #################################################
    # Print algebraic connectivity
    #################################################
    a_connectivity = algebraic_connectivity(G1)
    print("Algebraic connectivity of the graph:", a_connectivity)
    path_len = nx.average_shortest_path_length(G1)
    print("Average shortest path length of the graph:", path_len)

    #################################################
    # Print Kirchhof index
    #################################################
    kf_index = kirchhoff_index(G1)
    print("Kirchhoff index of the graph:", kf_index)

    #################################################
    # Print number of spanning trees
    #################################################
    eigenvalues = nx.linalg.spectrum.laplacian_spectrum(G1)
    sorted_eigenvalues = np.sort(eigenvalues)[::-1]
    num_spanning_trees = np.prod(sorted_eigenvalues[:-1]) / len(sorted_eigenvalues)
    formatted_num_spanning_trees = '{:.6f}'.format(num_spanning_trees)
    print("Number of Spanning Trees:", formatted_num_spanning_trees)

if __name__ == '__main__':
    file_path = "ibiza.net"
    G = nx.read_pajek(file_path, encoding='UTF-8')
    G1 = nx.Graph(G)

    print("Original graph:")
    calculations(G1)
    print("\n")

    #################################################
    # Example of node removal
    #################################################
    """G1.remove_node(1)
    print("After removing 1:")
    calculations(G1)
    print("\n")"""
