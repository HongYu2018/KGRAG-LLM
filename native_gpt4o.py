import os
from openai import OpenAI
import pandas as pd
import re

os.environ["OPENAI_API_KEY"] = "your key"

client = OpenAI()

def find_answer_gpt4o(question):
        
    prompt = f"""I have following question in the health condition domain.
    Question:
    {question}
    
    Your task is to use your best knowledge to provide the answer within one paragraph of 140 words.
    """
    
    completion = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": "Could you provide me the answer?"}
    ]
    )
    pgt4o_answer= completion.choices[0].message.content
    print(pgt4o_answer)
    return pgt4o_answer