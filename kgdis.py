import streamlit
from streamlit_agraph import agraph, Node, Edge, Config
from streamlit_agraph.config import Config, ConfigBuilder
from openai import OpenAI
import os
os.environ["OPENAI_API_KEY"] = "your key"

client = OpenAI()

def create_graph_nodes_edges(text):
    prompt = f"""
    I have the following text related to a medical condition. Create graph nodes and edges to represent the relationships between medical terms and key sentences in a structured format. The nodes should represent important medical terms and key concepts, and the edges should represent the relationships between them.

    Ensure the output follows this Python code format:
    nodes = []
    edges = []
    nodes.append(Node(id="Term1", label="Description1", size=25, shape="circularImage"))
    nodes.append(Node(id="Term2", label="Description2", size=25, shape="circularImage"))
    edges.append(Edge(source="Term1", label="relation", target="Term2"))

    Text:
    {text}

    Provide the nodes and edges in the specified Python code format.
    """

    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": "Provide me the graph"}
    ]
    )

    return completion.choices[0].message.content

# Read the content from the file
with open('retrieval.txt', 'r') as file:
    text_content = file.read()

# Create graph nodes and edges
graph_code = create_graph_nodes_edges(text_content)
print(graph_code)

config = Config(width=750,
                height=950,
                directed=True, 
                physics=True, 
                hierarchical=False,
                # **kwargs
                )

return_value = agraph(nodes=nodes, 
                      edges=edges, 
                      config=config)

# 1. Build the config (with sidebar to play with options) .
config_builder = ConfigBuilder(nodes)
config = config_builder.build()

# 2. If your done, save the config to a file.
config.save("config.json")

# 3. Simple reload from json file (you can bump the builder at this point.)
config = Config(from_json="config.json")

