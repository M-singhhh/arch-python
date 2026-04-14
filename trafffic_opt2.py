import networkx as nx 
import matplotlib.pyplot as plt 
import random

# 1. Setup Network Structure
nodes = ["A", "B", "C", "D"]
edges = [("A", "B"), ("B", "C"), ("C", "D"), ("A", "D"), ("B", "D")]

# Create a Directed Graph (DiGraph) to represent one-way traffic flow
G = nx.DiGraph()
G.add_nodes_from(nodes)

# Initialise edges with a starting density attribute
for u, v in edges:
    G.add_edge(u, v, density=random.uniform(0, 0.5))

# Use a spring layout for consistent node positioning across frames
pos = nx.spring_layout(G, seed=42) 

# 2. Define Physics/Flow Functions
def flow(d):
    """Calculates traffic flow based on density.
    Follows q = d * (1 - d) where 0=empty, 1=jammed."""
    return d * (1 - d)

def update_density(G):
    """Updates the density of all edges based on inflow and outflow."""
    # Store changes in a temp dict so updates don't interfere during the loop
    new_densities = {e: G.edges[e]['density'] for e in G.edges()}

    for u, v in G.edges():
        d = G.edges[u][v]['density']
        out_val = flow(d)
        
        # Traffic leaving this edge
        new_densities[(u, v)] -= out_val
        
        # Traffic entering successor edges (split evenly among neighbors)
        neighbours = list(G.successors(v))
        if neighbours:
            split = out_val / len(neighbours)
            for n in neighbours:
                new_densities[(v, n)] += split
    
    # Apply changes back to the graph with constraints [0, 1]
    for (u, v), val in new_densities.items():
        G[u][v]['density'] = max(0, min(1, val))

def generate_cars(G, entry_nodes):
    """Adds a small amount of new traffic at entry points."""
    for node in entry_nodes:
        for n in G.successors(node):
            G[node][n]['density'] = min(1, G[node][n]['density'] + random.uniform(0, 0.05))

# 3. Run Simulation & Save Frames
for t in range(50):
    generate_cars(G, ["A"]) # Inject traffic at node A
    update_density(G)       # Move traffic through the network
    
    # Visualization
    plt.clf() # Clear previous frame
    
    # Edge width is proportional to the current traffic density
    weights = [G[u][v]['density'] * 10 for u, v in G.edges()]
    
    nx.draw(G, pos, with_labels=True, width=weights, 
            node_color='skyblue', node_size=800, arrowsize=20)
    
    # Add a title to track progress
    plt.title(f"Traffic Simulation - Frame {t}")
    plt.savefig(f"frame_{t}.png")
