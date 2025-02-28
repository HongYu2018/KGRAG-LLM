import requests
from bs4 import BeautifulSoup
import json
import os

def get_disease_links():
    base_url = "https://www.nhs.uk/conditions/"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, "html.parser")

    links = []
    for link in soup.select("a[href^='/conditions/']"):
        href = link.get('href')
        if href and href.startswith('/conditions/') and href != '/conditions/':
            full_url = f"https://www.nhs.uk{href}"
            links.append(full_url)

    return links

def extract_section_data(soup, header_text):
    section = soup.find(lambda tag: tag.name in ["h2", "h3"] and header_text.lower() in tag.text.lower())
    if section:
        content = []
        for sibling in section.find_next_siblings():
            if sibling.name in ["h2", "h3"]:
                break
            if sibling.name == "p":
                content.append(sibling.get_text(strip=True))
            elif sibling.name == "ul":
                content.extend([li.get_text(strip=True) for li in sibling.find_all("li")])
        return content
    return []

def extract_disease_data(url):
    print('extract:', url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    #print(soup)
    
    paragraphs = soup.find_all('p')
    disease_data =''
    text = []
    # Extract and print the text from each <p> tag
    for p in paragraphs:
        print('I am ok')
        text_content=p.get_text()
        text.append(text_content)
        #print(text)
    
    return text

    #name = soup.find("h1").get_text(strip=True) if soup.find("h1") else "No name found"
    #symptoms = extract_section_data(soup, "Symptoms")
    #causes = extract_section_data(soup, "Causes")
    #treatments = extract_section_data(soup, "Treatments")
    
    # Example of body parts and severity extraction logic
    #body_parts = extract_section_data(soup, "Body parts")  # Assuming there's a section or use another approach
    #severity = extract_section_data(soup, "Severity")  # Same for severity

    #if symptoms and causes and treatments:
     #   disease_data = {
      #      "name": name,
       #     "symptoms": symptoms,
        #    "causes": causes,
         #   "treatments": treatments,
          #  "body_parts": body_parts,
           # "severity": severity
        #}
        #return disease_data
    #return disease_data

def save_diseases_to_json(diseases):
    if not os.path.exists("diseases"):
        os.makedirs("diseases")

    grouped_diseases = {}
    for disease in diseases:
        first_letter = disease["name"][0].upper()
        if first_letter not in grouped_diseases:
            grouped_diseases[first_letter] = []
        grouped_diseases[first_letter].append(disease)

    for letter, diseases_list in grouped_diseases.items():
        with open(f"diseases1/{letter}.json", "w") as outfile:
            json.dump(diseases_list, outfile, indent=4)

if __name__ == "__main__":
    #disease_links = get_disease_links()
    diseases = []
    disease_links =["https://www.nhs.uk/conditions/pneumonia/"]
    print (disease_links)
    
    for url in disease_links:
        disease_data = extract_disease_data(url)
        diseases.append(disease_data)
    
    print (diseases)

    # Check if "Acne" is in the diseases list, if not add it manually
    
