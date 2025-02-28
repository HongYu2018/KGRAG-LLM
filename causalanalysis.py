import rdflib
import networkx as nx
import matplotlib.pyplot as plt
from urllib.parse import urlparse

# Load the RDF data from the TTL file
file_path = 'kg.ttl'  # Path to the TTL file
graph = rdflib.Graph()
graph.parse(file_path, format='ttl')

# Function to extract the core term name without the URL prefix
def extract_name(term):
    if isinstance(term, rdflib.URIRef):
        return urlparse(term).path.split('/')[-1] or urlparse(term).fragment.split('/')[-1]
    return str(term)

# Initialize a directed graph for causality relationships
G = nx.DiGraph()

# Define causality relationship predicates
causality_predicates = ['caused_by', 'may_cause', 'causes', 'example', 'progression', 'causes', 'possible_cause']

# Extract and filter causality relationships involving pneumonia
for s, p, o in graph:
    predicate = extract_name(p).lower()
    if any(causal in predicate for causal in causality_predicates):
        subject = extract_name(s)
        obj = extract_name(o)
        if 'pneumonia' in subject.lower() or 'pneumonia' in obj.lower():
            # Add nodes and direct edges to the graph
            G.add_node(subject)
            G.add_node(obj)
            G.add_edge(subject, obj, label=predicate)

# Apply transitivity inference to identify indirect causal relationships
inferred_edges = set()

for source in G.nodes:
    for target in G.nodes:
        if source != target and nx.has_path(G, source, target):
            paths = list(nx.all_simple_paths(G, source, target))
            for path in paths:
                if len(path) > 2:  # A transitive relationship exists if the path length is greater than 2
                    inferred_edges.add((path[0], path[-1]))

# Add inferred transitive relationships to the graph
for (source, target) in inferred_edges:
    if not G.has_edge(source, target):
        G.add_edge(source, target, label='inferred_cause')

# Visualize the causality relationship graph
pos = nx.spring_layout(G, k=0.5)
plt.figure(figsize=(14, 16))
nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue', alpha=0.8)
nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=15, edge_color='gray', alpha=0.7)
nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')

# Draw edge labels to indicate causality and inferred relationships
edge_labels = {(s, o): d['label'] for s, o, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, label_pos=0.5)
plt.title("Causality Relationship Graph for Pneumonia")

# Save and display the graph
plt.savefig('kgimages/pneumonia_transitive_causality_graph.png', format='png')
plt.show()
