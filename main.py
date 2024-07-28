import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Arcade Ticket Calculator", layout="wide")

items = [
    {"name": "Pile of stickers", "price": "1", "times": "10"},
    {"name": "Sticker of your choice", "price": "2", "times": "10"},
    {"name": "E-fidgets Made by Micha!", "price": "3", "times": "1"},
    {"name": "OpenAI credits worth $10", "price": "4", "times": "10"},
    {"name": "Domain for 1 year", "price": "4", "times": "10"},
    {"name": "Good Sci-Fi Book", "price": "4","times": "1"},
    {"name": "Github Notebook", "price": "5", "times": "1"},
    {"name": "Logic Analyzer", "price": "5", "times": "5"},
    {"name": "USB-C Charger", "price": "6", "times": "1"},
    {"name": "Breadboard + jumper wires", "price": "6","times": "10"},
    {"name": "Multimeter", "price": "7","times": "5"},
    {"name": "Arcade Ticket Counter (Timer)", "price": "7","times": "1"},
    {"name": "Soldering iron + solder", "price": "8","times": "5"},
    {"name": "Helping hands", "price": "9","times": "1"},
    {"name": "Raspberry Pi Zero 2 W", "price": "10","times": "1"},
    {"name": "Pinecil", "price": "14","times": "1"},
    {"name": "YubiKey", "price": "15","times": "5"},
    {"name": "GitHub Keycaps x8", "price": "15","times": "1"},
    {"name": "Octocat Plushie", "price": "15","times": "1"},
    {"name": "Tuxedo pick set + clear training lock", "price": "18", "times": "1"},
    {"name": "Leatherman Skeletool", "price": "25", "times": "1"},
    {"name": "Wacom Intuos S", "price": "25", "times": "1"},
    {"name": "Logitech Mouse MX Anywhere 2S", "price": "25", "times": "1"},
    {"name": "Keychron K6 Pro", "price": "50", "times": "1"},
    {"name": "Ryobi Rotary Tool Kit", "price": "55", "times": "1"},
    {"name": "Ryobi 4 Tool Combo Kit", "price": "55", "times": "1"},
    {"name": "Samsung T7 1TB SSD (1,050MB/s, beige)", "price": "59", "times": "1"},
    {"name": "Invertocat Backpack MIIR", "price": "70", "times": "1"},
    {"name": "Flipper Zero", "price": "70", "times": "1"},
    {"name": "Logitech MX Mechanical", "price": "75", "times": "1"},
    {"name": "Wacom One display", "price": "90", "times": "1"},
    {"name": "Nvidia Tesla P40 GPU (24GB GDDR5)", "price": "120" ,"times": "1"},
    {"name": "Prusa MINI+", "price": "130" ,"times": "1"},
    {"name": "Bambu Lab A1 mini", "price": "135" ,"times": "1"},
    {"name": "AirPods Pro. Refurbished", "price": "140" ,"times": "1"},
    {"name": "iPad 10th Gen + 1st Gen Apple Pencil", "price": "160" ,"times": "1"},
    {"name": "ThinkPad T490 (14-inch model)", "price": "168" ,"times": "1"},
    {"name": "Quest 3", "price": "200" ,"times": "1"},
    {"name": "RTX 3090 (24GB GDDR6). Used", "price": "280" ,"times": "1"},
    {"name": "MacBook Air M2", "price": "400" ,"times": "1"}
]

st.markdown("""
    <nav style="background-color: #f8f9fa; padding: 1rem;">
        <h1 style="text-align: center; margin: 0;color: black">Arcade Ticket Calculator</h1>
    </nav>
""", unsafe_allow_html=True)

st.write("## Select Prizes and Enter Your Tickets")


selected_prizes_counts = {}


prize_options = []
for item in items:
    for i in range(int(item['times'])):
        prize_options.append(f"{item['name']} ({item['price']} tickets)")


selected_prizes = st.multiselect("Choose prizes:", prize_options)


for prize in selected_prizes:
    item_name = prize.split(" (")[0]
    if item_name in selected_prizes_counts:
        selected_prizes_counts[item_name] += 1
    else:
        selected_prizes_counts[item_name] = 1

tickets = st.number_input("Enter the number of tickets you have:", min_value=0, step=1)

if selected_prizes_counts and tickets is not None:
    total_price = sum(int(item['price']) * count for item in items if item['name'] in selected_prizes_counts for count in [selected_prizes_counts[item['name']]])
    st.write(f"You have selected the following prizes:")
    for prize, count in selected_prizes_counts.items():
        st.write(f"- {prize} x {count}")
    st.write(f"Total tickets required: {total_price}")

    days_remaining = (datetime.strptime("2024-08-31", "%Y-%m-%d") - datetime.now()).days
    tickets_needed = total_price - tickets
    if tickets_needed > 0:
        tickets_per_day = tickets_needed / days_remaining
        st.write(f"You need to earn {tickets_per_day:.2f} tickets per day to reach your goal by 31st August.")
    else:
        st.write("You already have enough tickets to get your selected prizes!")
