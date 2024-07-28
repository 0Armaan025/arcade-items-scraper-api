import requests
from bs4 import BeautifulSoup
import time
import json
import re
import streamlit as st

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

def scrape_prizes(url):
    page_content = fetch_page(url)
    soup = BeautifulSoup(page_content, 'html.parser')

    pixel_prizes_section = soup.find(text="Pixel Prizes: 1-10 🎟️")

    if (parent_div := pixel_prizes_section.find_parent('div')):

        class_pattern = re.compile(r'slackey css-')
        price_pattern = re.compile(r'\d+<!-- --> 🎟️')


        prize_titles = parent_div.find_all('span', class_=class_pattern)

        prizes = []
        for title in prize_titles:

            title_text = title.get_text(strip=True)

         
            price_span = title.find_next_sibling('span', class_=class_pattern, text=price_pattern)
            price_text = price_span.get_text(strip=True) if price_span else "N/A"

            prizes.append((title_text, price_text))

        return prizes
    else:
        return []

url = "https://hackclub.com/arcade/shop/"
prizes = scrape_prizes(url)


st.set_page_config(page_title="Arcade Ticket Calculator", layout="wide")


st.markdown("""
    <nav style="background-color: #f8f9fa; padding: 1rem;">
        <h1 style="text-align: center; margin: 0;color: black">Arcade Ticket Calculator</h1>
    </nav>
""", unsafe_allow_html=True)


st.write("## Select a Prize and Enter Your Tickets")


prize_options = [f"{title} ({price})" for title, price in prizes]
selected_prize = st.selectbox("Choose a prize:", prize_options)
tickets = st.number_input("Enter the number of tickets you have:", min_value=0, step=1)


if selected_prize and tickets:
    st.write(f"You have selected **{selected_prize}** and entered **{tickets}** tickets.")
