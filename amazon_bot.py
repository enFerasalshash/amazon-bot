import sqlite3
import time
import requests
from bs4 import BeautifulSoup

DATABASE = 'deals.db'

def initialize_database():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS deals
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT,
                  price TEXT,
                  url TEXT)''')
    conn.commit()
    conn.close()

def fetch_amazon_deals():
    URL = 'https://www.amazon.com/s?k=deals'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    deals = []
    for item in soup.select('.s-main-slot .s-result-item'):
        title = item.select_one('h2 a span')
        price = item.select_one('.a-price .a-offscreen')
        url = item.select_one('h2 a')
        if title and price and url:
            deals.append({
                'title': title.get_text(),
                'price': price.get_text(),
                'url': f"https://www.amazon.com{url['href']}"
            })

    store_deals(deals)

def store_deals(deals):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    for deal in deals:
        c.execute('''INSERT INTO deals (title, price, url) VALUES (?, ?, ?)''', (deal['title'], deal['price'], deal['url']))
    conn.commit()
    conn.close()

def main():
    print("Starting the bot...")
    initialize_database()
    while True:
        print("Fetching Amazon deals...")
        fetch_amazon_deals()
        print("Fetched and stored Amazon deals.")
        print("Sleeping for 1 minute...")
        time.sleep(60)

if __name__ == '__main__':
    main()
