import requests
from bs4 import BeautifulSoup
import json
import re
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

def scrape_prizes_and_prices(url):
    page_content = fetch_page(url)
    soup = BeautifulSoup(page_content, 'html.parser')

    divs = soup.find_all('div')
    items = []
    seen_items = set()

    remove_patterns = [
        "All + 1", "E-fidgets Made by Micha!", "Notebook from GitHub",
        "USB-C Charger (30W)", "GitHub Keycaps", "Octocat", "55 + 55 tickets",
        "55 + 4 Tool Combo Kit tickets", "Samsung T7 1TB SSD", "Invertocat Backpack",
        "Logitech", "Nvidia Tesla P40 GPU", "AirPods Pro", "ThinkPad T490", "\ud83c\udf9f\ufe0f + 16 inch tickets",
        "\ud83c\udf9f\ufe0f + 13 inch tickets",
        "Framework factory seconds", "\ud83c\udf9f\ufe0f", "Framework 13 inch", "Framework 16 inch",
        "RTX 3090 + 1 tickets"
    ]

    for div in divs:
        texts = list(div.stripped_strings)
        for i, text in enumerate(texts):
            if re.match(r'\d+', text):  # Check if the text is a number (price)
                price = text
                if len(texts) > i + 2:  # Ensure there is a text_3 for the name
                    name = texts[i + 2]
                    item = f"{name} + {price} tickets"
                    if item not in seen_items and not any(pattern in item for pattern in remove_patterns):
                        items.append(item)
                        seen_items.add(item)
                break

    return items

url = "https://hackclub.com/arcade/shop/"
prizes_and_prices = scrape_prizes_and_prices(url)

# Print the final list of items with prices in JSON format
print(json.dumps(prizes_and_prices, indent=4))
