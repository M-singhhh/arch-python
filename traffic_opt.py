import networkx as nx 
import matplotlib.pyplot as plt 



nodes = ["A","B","C","D"]
edges = [("A","B"),("B","C"),("C","D"),("A","D"),("B","D")]

G = nx.DiGraph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)

pos = nx.spring_layout(G)

nx.draw(G , pos , with_labels = True ,node_size = 2000 , arrows = True )

plt.savefig("graph.png") 

