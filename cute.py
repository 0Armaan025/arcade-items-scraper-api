import requests
from bs4 import BeautifulSoup
import json
import time

def fetch_page(url, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  
            return response.content
        except requests.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2)  
    raise Exception(f"Failed to fetch the page after {retries} attempts.")

def scrape_all_divs(url):
    page_content = fetch_page(url)
    soup = BeautifulSoup(page_content, 'html.parser')
    

    divs = soup.find_all('div')

    div_data = []
    for div in divs:
        div_info = {
            "text": div.get_text(strip=True),
            
        }
        div_data.append(div_info)
    
    return div_data

url = "https://hackclub.com/arcade/shop/"
div_data = scrape_all_divs(url)


print(json.dumps(div_data, indent=4))
