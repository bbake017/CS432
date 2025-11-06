import matplotlib.pyplot as plt
import networkx as nx

karateGraph = nx.karate_club_graph()

color = ["#1f78b4"] * 34
color[0] = "green"  # Mr. Hi
color[1] = "green"
color[2] = "green"
color[3] = "green"
color[4] = "green"
color[5] = "green"
color[6] = "green"
color[7] = "green"
color[8] = "green"
color[9] = "red"
color[10] = "green"
color[11] = "green"
color[12] = "green"
color[13] = "green"
color[14] = "red"
color[15] = "red"
color[16] = "green"
color[17] = "green"
color[18] = "red"
color[19] = "green"
color[20] = "red"
color[21] = "green"
color[22] = "red"
color[23] = "red"
color[24] = "red"
color[25] = "red"
color[26] = "red"
color[27] = "red"
color[28] = "red"
color[29] = "red"
color[30] = "red"
color[31] = "red"
color[32] = "red"
color[33] = "red"   # John

# Initial Graph
print("Initial Graph:")
nx.draw_kamada_kawai(karateGraph, with_labels=True, node_color=color)
plt.show()  

iter = 0
while(karateGraph.number_of_edges() > 0 and nx.number_connected_components(karateGraph) < 2): # The alogorithm
    iter += 1

    allEdgesBetweenList = nx.edge_betweenness_centrality(karateGraph, k=None, normalized=True, weight=None, seed=None)
    maxEdge = max(allEdgesBetweenList, key=allEdgesBetweenList.get)

    print(f"Highest edge betweenness value: {maxEdge} : {allEdgesBetweenList[maxEdge]}") 
    print(f"Iteration #{iter} ")

    karateGraph.remove_edge(maxEdge[0], maxEdge[1]) # Remove edge with largest edge betweenenss value

    #nx.draw_kamada_kawai(karateGraph, with_labels=True, node_color=color)
    #plt.show()
    

print(f"This took {iter} iterations")
nx.draw_networkx(karateGraph, with_labels=True, node_color=color)
plt.show()