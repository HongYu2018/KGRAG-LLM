import os
from openai import OpenAI
import pandas as pd
import re


os.environ["OPENAI_API_KEY"] = "your key"

client = OpenAI()

def find_related_kg(query):
    with open('kg.ttl', 'r', encoding='utf-8') as f:
        content_kg = f.read()
        
    prompt = f"""I have the following Knowledge Graph data that related medical conditions learnt from the answers provided by NHS website.

    Knowledge Graph data:
    {content_kg}
    
    Your task is to take the following Query related medical condition question as input to extract useful information by parsing the Knowledge Graph triples to restructure the related triples as the text ouput.
    
    Query:
    {query}
    """
    
    completion = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": "Provide me the related output."}
    ]
    )
    kg_content= completion.choices[0].message.content
    print(kg_content)
    f.close
    return kg_content

#find_related_kg('What are the symptoms of anxiety?')