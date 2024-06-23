import sys

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from networkx import draw_spring, resistance_distance


def kirchhoff_index(G):
    #################################################
    # Obtain Kirchhof index
    #################################################
    n = len(G.nodes)
    Kf = 0
    for u in range(n):
        for v in range(u + 1, n):
            Kf += resistance_distance(G, list(G.nodes)[u], list(G.nodes)[v])
    return Kf

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python Main.py <file_name>")
        sys.exit(1)

    file_path = sys.argv[1]

    G = nx.read_pajek(file_path, encoding='UTF-8')
    G1 = nx.Graph(G)

    #################################################
    # Print laplacian eigenvalues
    #################################################
    eigenvalues = nx.linalg.spectrum.laplacian_spectrum(G)

    #################################################
    # Sort the eigenvalues in descending order
    #################################################
    sorted_eigenvalues = np.sort(eigenvalues)[::-1]

    #################################################
    # Format to avoid scientific notation and round to 6 decimal places
    #################################################
    formatted_eigenvalues = [f"{eig:.6f}" for eig in sorted_eigenvalues]
    print("Laplacian Eigenvalues (sorted and rounded):\n", formatted_eigenvalues)
    print("\n")
    num_spanning_trees = np.prod(sorted_eigenvalues[:-1]) / len(sorted_eigenvalues)

    #################################################
    # Format the number of spanning trees to avoid scientific notation
    #################################################
    formatted_num_spanning_trees = '{:.6f}'.format(num_spanning_trees)
    print("Number of Spanning Trees:", formatted_num_spanning_trees)
    print("\n")

    #################################################
    #Print Kirchhof index
    #################################################
    kirchhoff_index = kirchhoff_index(G1)
    print("Kirchhoff index of the graph:", kirchhoff_index)
    print("\n")

    #################################################
    # Print adjacency matrix eigenvalues
    #################################################
    adj_matrix = nx.to_numpy_array(G1)
    adj_eigenvalues = np.linalg.eigvals(adj_matrix)

    #################################################
    # Convert to real if close
    #################################################
    real_adj_eigenvalues = np.real_if_close(adj_eigenvalues, tol=1e-5)
    sorted_adj_eigenvalues = np.sort(real_adj_eigenvalues)[::-1]

    #################################################
    # Format to avoid scientific notation and round to 6 decimal places
    #################################################
    formatted_adj_eigenvalues = [f"{eig:.6f}" for eig in sorted_adj_eigenvalues]
    print("Eigenvalues of the adjacency matrix (sorted and rounded):\n", formatted_adj_eigenvalues)

    #################################################
    # Show graph with labels
    #################################################
    draw_spring(G1, with_labels=True)
    plt.show()

