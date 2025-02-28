from haystack.document_stores.in_memory import InMemoryDocumentStore
from datasets import load_dataset
from haystack import Document
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.builders import PromptBuilder
import os
from getpass import getpass
from haystack.components.generators import OpenAIGenerator
from haystack import Pipeline
import urllib.request as urllib2

from haystack import PredefinedPipeline

import requests

from bs4 import BeautifulSoup

from openai import OpenAI
import pandas as pd
import json
import re
import kgagent as kga
import nhsapi as nhs
import time

# URL of the NHS webpage
#url = 'https://www.nhs.uk/conditions/kidney-stones/'

os.environ["OPENAI_API_KEY"] = "your key"

client = OpenAI()

def query_response(query):
    # URL of the NHS conditions page
    url = "https://www.nhs.uk/conditions/"

    # Send an HTTP request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")
    
        # Find the ordered list containing the conditions
        ordered_lists = soup.find_all('ol', class_='nhsuk-list')
        #conditions_list = soup.find_all('ul', class_='nhsuk-list nhsuk-list--border')
    
        # Find all list items and extract condition names from anchor tags
        diseases = []
        # Select the second ordered list
        print_number=0
        if len(ordered_lists) > 1:
            conditions_list = ordered_lists[1]
            #print(conditions_list)
            list_items = conditions_list.find_all('ul', class_='nhsuk-list nhsuk-list--border')
            #print(list_items)
            for item in list_items:
                ix = item.find_all('li')
                for itx in ix:
                    link = itx.find('a')
                    if link:
                        disease = link.get_text(strip=True)+';'+link['href']
                        #diseases.append(link.get_text(strip=True))
                        diseases.append(disease)
        print(len(diseases))
        # Display the disease names
        #for disease in diseases:
            #if print_number < 150 and print_number > 119:
                #print(disease)
            #print_number = print_number+1
    else:
        print("Failed to retrieve the page.")
    
    list_c = ''
    
    #invoke knowledge graph agent to get leant knowledge
    st = time.time()
    content_kg = kga.find_related_kg(query)
    et = time.time()
    # get the execution time
    elapsed_time = et - st
    print('KG Execution time:', elapsed_time, 'seconds')
    
    #print(content_kg)

    completion = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[
            #{"role": "system", "content": "You are a disease web link retriver which you need to find the most related web links related to a question or a medical term in the query context from NHS A-Z website with link here: https://www.nhs.uk/conditions/. You only need to have the web links from NHS in seperated by ',' as a string data and without any further comments or explanations."},
            #{"role": "user", "content": "here is the query: " +query+ " Can you get all the related web url links?"}
            {"role": "system", "content": "You are a web link search engine and you need to find the most related web links from the list of " + ','.join(diseases) + " based on the give query by the user and important pre-knowledge from "+content_kg+". You only need to have the web links from the list data with seperation by ',' as a string data and without any human language such as further comments or explanations."},
            {"role": "user", "content": "here is the query: " +query+ " Can you get all the related web url links?"}
        ]
    )
    string_c= completion.choices[0].message.content
    #print(string_c)
    list_c=string_c.split(',')
    #print(list_c)
    #get url_list suggested by agent to web reader to get the content#
    content_r = ''
    for url_list in list_c:
        #print('exracting from:',url_list)
        if len(url_list.split('/'))>2: 
            condition_name=url_list.split('/')[2]
        
        print('condition is:',condition_name)
        #disease_data = extract_disease_data('https://www.nhs.uk'+url_list)
        disease_data = nhs.get_nhsapi_content(condition_name)
        content_r=content_r + ' ' + ''.join(disease_data)
    #covid19_1 = nhs.get_nhsapi_content()
    
    #print(content_r)
    #with open('kg.ttl', 'r', encoding='utf-8') as f:
     #   content_kg = f.read()

    with open('retrieval.txt', 'w', encoding='utf-8') as f:
        f.write(f"{content_kg}\n{content_r}")

    indexing_pipeline =  Pipeline.from_template(PredefinedPipeline.INDEXING)
    indexing_pipeline.run(data={"sources": ["retrieval.txt"]})

    rag_pipeline =  Pipeline.from_template(PredefinedPipeline.RAG)
    
    query = query

    result = rag_pipeline.run(data={"prompt_builder": {"query":query}, "text_embedder": {"text": query}})
    responses = result["llm"]["replies"][0]
    print(responses)
    #print(list_c)
    return responses, list_c

def extract_disease_data(url):
    #print('extract:', url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    #print(soup)
    
    paragraphs = soup.find_all('p')
    disease_data =''
    text = []
    # Extract and print the text from each <p> tag
    for p in paragraphs:
        #print('I am ok')
        text_content=p.get_text()
        text.append(text_content)
        #print(text)
    
    return text
