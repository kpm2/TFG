import sys
import networkx as nx
from networkx import betweenness_centrality, closeness_centrality, katz_centrality, pagerank

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <read_file_path> <write_file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    file_path2 = sys.argv[2]
    G = nx.read_pajek(file_path, encoding='UTF-8')
    G1 = nx.Graph(G)

    #################################################
    #Calculate betweenness centrality
    #################################################
    betweenness_centrality = betweenness_centrality(G)
    betweenness = list(betweenness_centrality.values())

    #################################################
    #Calculate closeness centrality
    #################################################
    closeness_centrality=closeness_centrality(G)
    closeness = list(closeness_centrality.values())

    #################################################
    #Calculate katz centrality
    #################################################
    katz_centrality = katz_centrality(G1)
    katz = list(katz_centrality.values())

    #################################################
    #Calculate pagerank centrality
    #################################################
    pagerank = pagerank(G, weight=None)
    pr = list(pagerank.values())

    is_vertices_section = False
    count = 0

    with open(file_path, 'r') as reader:
        with open(file_path2, 'w') as writer:
            writer.write('Id, Name, Lat, Long, Betweenness, Closeness, Katz, Pagerank\n')
            for line in reader:
                #################################################
                # Start printing when reaching vertices section
                #################################################
                if line.startswith("*Vertices"):
                    is_vertices_section = True
                #################################################
                # Stop printing when reaching edges section
                #################################################
                elif line.startswith("*Edges"):
                    is_vertices_section = False
                elif is_vertices_section:
                    split_line=line.split("\"")
                    split_line2=split_line[2].split(" ")
                    writer.write(split_line[0].strip(" ") + ", " + split_line[1] + ", " + split_line2[2] + ", "
                                 + split_line2[1] + ", " + str(betweenness[count]) + ", " + str(closeness[count]) +
                                 ", " + str(katz[count]) + "," + str(pr[count]) + "\n")
                    count += 1