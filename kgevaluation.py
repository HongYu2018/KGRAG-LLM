import rdflib
from rdflib.namespace import RDF
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import os
from urllib.parse import urlparse

# Define a function to strip URL prefixes from terms
def extract_name(term):
    if isinstance(term, rdflib.URIRef):
        return urlparse(term).path.split('/')[-1] or urlparse(term).fragment.split('/')[-1]
    return str(term)

# Load the RDF file and set up the save directory
file_path = 'kg.ttl'  # Update with the correct path if necessary
save_dir = 'kg1images'
os.makedirs(save_dir, exist_ok=True)

# Parse the RDF file
graph = rdflib.Graph()
graph.parse(file_path, format='ttl')

# Count the total number of triples
num_triples = len(graph)

# Extract and process terms and relations
terms = set()
relations = set()
for s, p, o in graph:
    terms.add(extract_name(s))
    terms.add(extract_name(o))
    relations.add(extract_name(p))

# Count the number of terms and unique relations
num_terms = len(terms)
num_relations = len(relations)

# Output the results
print(f"Total number of terms: {num_terms}")
print(f"Total number of triples: {num_triples}")
print(f"Total number of unique relations: {num_relations}")

# Initialize the NetworkX graph
G = nx.DiGraph()

# Add nodes and edges to the graph with stripped terms and relations
for s, p, o in graph:
    s_name = extract_name(s)
    o_name = extract_name(o)
    p_name = extract_name(p)
    G.add_node(s_name)
    G.add_node(o_name)
    G.add_edge(s_name, o_name, label=p_name)

# Define the layout for the graph visualization
pos = nx.spring_layout(G, k=0.15)

# Draw the graph
plt.figure(figsize=(20, 20))
nx.draw_networkx_nodes(G, pos, node_size=500, node_color='skyblue', alpha=0.7)
nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=10, edge_color='gray', alpha=0.5)
nx.draw_networkx_labels(G, pos, font_size=8)

# Draw edge labels for relationships
edge_labels = {(s, o): d['label'] for s, o, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6, label_pos=0.5)
plt.title("RDF Graph Visualization (Stripped URLs)")

# Save and display the graph visualization
term_save_path = os.path.join(save_dir, 'rdfgv.png')
plt.savefig(term_save_path, format='png')
plt.close()

# Count occurrences of each relation type
relation_counts = Counter(relations)

# Bar plot for relation distribution
plt.figure(figsize=(10, 6))
plt.bar(relation_counts.keys(), relation_counts.values(), color='orange')
plt.xlabel('Relation Types')
plt.ylabel('Frequency')
plt.title('Distribution of Relation Types')
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

# Save and display the relation distribution plot
relation_save_path = os.path.join(save_dir, 'distribution_relation_types.png')
plt.savefig(relation_save_path, format='png')
plt.close()

# Bar plot for term counts (top 20 most frequent terms)
term_counts = Counter(terms)
common_terms = term_counts.most_common(20)

plt.figure(figsize=(10, 6))
plt.bar([term[0] for term in common_terms], [count[1] for count in common_terms], color='green')
plt.xlabel('Terms')
plt.ylabel('Frequency')
plt.title('Top 20 Most Frequent Terms')
plt.xticks(rotation=90, ha="right")
plt.tight_layout()

# Save and display the term frequency plot
term_save_path = os.path.join(save_dir, '20FT.png')
plt.savefig(term_save_path, format='png')
plt.close()

