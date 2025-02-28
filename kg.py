from openai import OpenAI
import os
import json
from rdflib import Graph, URIRef, Literal, Namespace
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

    Provide the nodes and edges in a JSON formate that must be validated JSON file. Remember no further comments or explanations are needed to add to the file only the pure JSON data and '''json are needed.
    """

    completion = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": "Provide me the graph notes.json file"}
    ]
    )
    json_output = completion.choices[0].message.content
    j_list=json_output.split("json")
    if len(j_list)>0:
        json_output = json_output[7:-3]
        #print(json_output)
    json_to_rdf(json_output)
    return json_output

def json_to_rdf(json_output, rdf_file="kg.ttl"):
    
    json_data = json.loads(json_output)
    # Create a new RDF graph
    g = Graph()

    # Load the existing RDF data from the file if it exists
    if os.path.exists(rdf_file):
        g.parse(rdf_file, format="turtle")

    # Define a namespace for your RDF data
    ex = Namespace("http://diseaseknowledge.org/")
    rdfex = Namespace("http://www.w3.org/TR/rdf11-schema/")
    wikiex = Namespace("https://en.wikipedia.org/wiki/")

    # Add nodes as RDF subjects, ignoring 'size' and 'shape' attributes
    for node in json_data.get('nodes', []):
        node_id = node.get('id').replace(' ','_')
        node_label = node.get('label').replace(' ','_')
        
        # Create RDF subject for the node (URIRef)
        node_uri = URIRef(ex[node_id])
        
        # Add label property (if available)
        if node_label:
            target_uri = URIRef(wikiex[node_label])
            if node_id == node_label:
                g.add((node_uri, ex.label, target_uri))
            #g.add((node_uri, ex.label, Literal(node_label)))
            else:
                g.add((node_uri, rdfex.type, target_uri))

    # Add edges as RDF predicates and objects
    for edge in json_data.get('edges', []):
        source = edge.get('source').replace(' ','_')
        target = edge.get('target').replace(' ','_')
        label = edge.get('label').replace(' ','_')
        
        # Create RDF subjects and objects
        source_uri = URIRef(ex[source])
        target_uri = URIRef(ex[target])
        
        # Add the edge as a triple
        if label:
            g.add((source_uri, URIRef(ex[label]), target_uri))

    # Serialize the updated graph in RDF Turtle format
    g.serialize(destination=rdf_file, format='turtle')

    print(f"RDF data updated and saved to {rdf_file}")

# Read the content from the file
#text_content=""
#with open('test_data.txt', 'r') as file:
    #text_content = file.read()

#create_graph_nodes_edges(text_content)