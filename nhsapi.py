import requests
import json

def get_nhsapi_content(condition_name):
    base_url = "https://api.nhs.uk/conditions"
    #condition = "lung-cancer"  # Specify the condition here
    full_url = f"{base_url}/{condition_name}"

    # Your subscription key for the API
    subscription_key = "6408043d4ae444e69ea5bb3842931910"  # Replace with your actual key

    # Set up the headers including your subscription key
    headers = {
        "subscription-key": subscription_key
    }

    # Optional: Add any query parameters (e.g., for modules)
    params = {
        #"modules": "true"  # Set to 'true' if you want to include modules
        "childArticles": "true"  # Set to 'true' if you want to include modules
    }

    # Make the GET request
    response = requests.get(full_url, headers=headers, params=params)
    

    # Check if the request was successful
    if response.status_code == 200:
        # Parse and print the JSON content
        content = response.json()
        #print(content)
        data = content
    
        main_description = data.get('description', '')
        #print("Main Description:", main_description)
        full_text_content = main_description
    
        main_entity_texts = []
        if 'mainEntityOfPage' in data:
            main_entity_texts.extend(extract_text_sections(data['mainEntityOfPage']))
    
            # Combine and clean up extracted text for easier reading
            full_text_content = "\n\n".join(main_entity_texts)
        #print("Full Text Content:\n", full_text_content)
        response = full_text_content
    else:
        # Print an error message if the request failed
        print(f"Failed to retrieve data: {response.status_code}")
        response = ''
        #print(response.text)  
    #data = json.loads(content)
    
    return response

    # Function to extract text content from nested 'mainEntityOfPage' or 'hasPart'
def extract_text_sections(entity_list):
    text_content = []
    for entity in entity_list:
        if 'text' in entity:
            text_content.append(entity['text'])
        # Recursively check for nested mainEntityOfPage or hasPart
        if 'mainEntityOfPage' in entity:
            text_content.extend(extract_text_sections(entity['mainEntityOfPage']))
        if 'hasPart' in entity:
            text_content.extend(extract_text_sections(entity['hasPart']))
    return text_content

#text = get_nhsapi_content('covid-19-symptoms-and-what-to-do')
#print(text)

 