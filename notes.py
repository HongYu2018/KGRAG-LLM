from openai import OpenAI
import os
import json
import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from streamlit_agraph.config import Config, ConfigBuilder
import ragpipeline as rag
import kg
os.environ["OPENAI_API_KEY"] = "your key"

client = OpenAI()


def create_graph_nodes_edges(text_content):
    prompt = f"""
    I have the following text related to a medical condition. First summerise the keywords that present the condition names, symptome names, treatment names, prevention method names, diagnosing method names and who is at rick from the conditions. Then, create graph nodes and edges to represent the relationships between key medical terms that relation maximumly include [disease names, possible cause, symptoms, treatment, diagnosing, Preventing, Who's at risk] in a structured format. The nodes should only represent important medical terms without any descriptive or verb words and key concepts, and the edges should represent the relationships between them.

    Ensure the output is a validate JSON file that can easily be read and transfoer to the following Python code format:
    nodes = []
    edges = []
    nodes.append(Node(id="Term1", label="Description1", size=25, shape="circularImage"))
    nodes.append(Node(id="Term2", label="Description2", size=25, shape="circularImage"))
    edges.append(Edge(source="Term1", label="relation", target="Term2"))

    Text:
    {text_content}

    Provide the nodes and edges in a JSON formate that must be validated JSON file. Remember no further comments or explanations are needed to add to the file only the pure JSON data no '''json are needed.
    """

    completion = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": "Provide me the graph notes.json file"}
    ]
    )

    return completion.choices[0].message.content

st.title('🦜🔗 Quickstart Health Condition Checking')

with st.form('my_form'):
    text = st.text_area('Enter your query:', 'What is the major cause of Pneumonia?')
    submitted = st.form_submit_button('Submit')
    if submitted:
        output,data_s = rag.query_response(text)
        st.text_area('Query result:', output)
        st.text_area('Data sources:', data_s)

        # Read the content from the file
        with open('retrieval.txt', 'r') as file:
            text_content = file.read()

        # Create graph nodes and edges
        graph_notes = kg.create_graph_nodes_edges(text_content)
        print(graph_notes)
        
        graph_notes_t = graph_notes

        #data = json.loads(graph_notes[7:-3])
        data = json.loads(graph_notes)

        nodes = []
        edges = []

        # Convert JSON nodes to Node objects and append to the nodes list
        for node in data["nodes"]:
            nodes.append(Node(id=node["id"], label=node["label"], size=node["size"], shape=node["shape"], image="C:/Users/301054/Documents/RAGLLM/di.png"))

        # Convert JSON edges to Edge objects and append to the edges list
        for edge in data["edges"]:
            edges.append(Edge(source=edge["source"], label=edge["label"], target=edge["target"]))

        # Output the nodes and edges
        print("Nodes:")
        for node in nodes:
            print(node)

        print("\nEdges:")
        for edge in edges:
            print(edge)
    
        # Output the nodes and edges
        print("Nodes:")
        for node in nodes:
            print(node)

        print("\nEdges:")
        for edge in edges:
            print(edge)

        #Create graph nodes and edges
        #graph_code = create_graph_nodes_edges(text_content)
        graph_code = graph_notes_t
        
        #print(graph_code)

        config = Config(width=1000,
                        height=900,
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