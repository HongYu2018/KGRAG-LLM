import os
from openai import OpenAI
import ragpipeline as rag
import kg
import native_gpt4o as gpt
import time

os.environ["OPENAI_API_KEY"] = "your key"

client = OpenAI()

def examiner_scoring(question,answer):
    with open('testing_data\groundtruth_rsv.txt', 'r', encoding='utf-8') as f:
        ground_truth = f.read()
        
    prompt = f"""You are an expert evaluator responsible for assessing the accuracy of an answer provided by an AI system. Your task is to identify any sentences in the answer that contain information not validated or incorrect according to the ground truth.

    Criteria for unvalidated information:
    - Any information that is inaccurate or contradicts the ground truth content, but you need to make sure your evaluation is correct.
    - Any information that is misleading or lacks verification based on the ground truth provided.
    - If the information does not have similar meaning in the ground truth, it should be flagged.
    
    Importantly, not just do word marching evaluation but work on meaning evaluation. For example, if the answer is 'cough' and ground truth is a 'persistent cough', then the meaning is validate and content is correct. 

    Your task is to review the answer and list issues that include unvalidated or incorrect information according to the ground truth. Output each of these contents (words or sentences), separated by "::".

    Input:

    Question: {question}
    Ground truth related information: {ground_truth}
    Given answer: {answer}

    Output:

    List of unvalidated information from the answer according to the ground truth and separated by "::".
    """
    
    completion = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": "Could you provide me the output?"}
    ]
    )
    score= completion.choices[0].message.content
    #print(score)
    f.close
    return score
question = "What are the symptoms of respiratory syncytial virus and how to avoid?"

st = time.time()
answer, list_d = rag.query_response(question)
et = time.time()
# get the execution time
elapsed_time = et - st
print('Execution time:', elapsed_time, 'seconds')

with open('retrieval.txt', 'r') as file:
    text_content = file.read()
kg.create_graph_nodes_edges(text_content)
#final_score_1 = examiner_scoring(question,answer)
#sentence_n_1 = len(answer.split(" "))
#score1 = len(final_score_1.split("::"))
#print("RAG-KG answer score: ",score1/140)
#print(score1,final_score_1)

#st = time.time()
#gpt_answer = gpt.find_answer_gpt4o(question)
#et = time.time()
# get the execution time
#elapsed_time = et - st
#print('Execution time:', elapsed_time, 'seconds')

#final_score_2 = examiner_scoring(question,gpt_answer)
#sentence_n_2 = len(gpt_answer.split(" "))
#score2 = len(final_score_2.split("::"))
#We ask all the agent to answer the question in 140 words. So we can assume that the maximum lenth of the answer is 140. 
#print("GPT-4o answer score: ",score2/140)
#print(score2,final_score_2)



