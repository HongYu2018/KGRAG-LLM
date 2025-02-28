import requests
from bs4 import BeautifulSoup

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

    # Display the disease names
    for disease in diseases:
        if print_number < 150 and print_number > 119:
            print(disease)
        print_number = print_number+1
else:
    print("Failed to retrieve the page.")