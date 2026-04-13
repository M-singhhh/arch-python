import networkx as nx 
import matplotlib.pyplot as plt 
import random


nodes = ["A","B","C","D"]
edges = [("A","B"),("B","C"),("C","D"),("A","D"),("B","D")]

# I used networkx lib to create a graph of nodes and edges which we will se as path of roads here is 
# networkx doc  -> https://networkx.org/documentation/stable/reference/introduction.html#networkx-basics


G = nx.DiGraph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)

pos = nx.spring_layout(G)

#now we are adding density to edges that will represent the flow of traffic 
for u,v in edges:
    G.add_edge(u,v,density=0.0)

for u,v in G.edges():
    G[u][v]['density'] = random.uniform(0,1)

#Making the density added visible to the graph  
edge_lables = {
    (u,v) : f"{G[u][v]['density']:.2f}"
for u,v in G.edges()
}

#drawing graph 
weights = [G[u][v]['density']*5 for u,v in G.edges()] # this will decide the width of the edge if there is more traffic density then edge width will be thick otherwise thin 
nx.draw(G , pos , with_labels = True ,node_size = 2000 ,width = weights, arrows = True )
nx.draw_networkx_edge_labels(G,pos, edge_labels = edge_lables)
plt.savefig("graph.png") 

def flow(d):
    return d*(1-d) #this will return the the flow while density is the parameter it takes 
#how it works ? --> flow = how many car exist * how fast are they moving = density * velocity 
# and as velocity inversely prop density so we replace velocity with function of density 
#  why we took only this func d*(d-1) cause at medium density flow will be the best which this function staisfies 
# we can take any function into account which follow this constraints q (0) = 0 & q(1) = 0 cause no cars no flow and jam no flow either 

