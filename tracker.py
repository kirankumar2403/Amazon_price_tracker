import requests
from bs4 import BeautifulSoup
import csv
import time
import schedule
from alert import send_email_alert
from datetime import datetime
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

def read_products(filename="products.csv"):
    products = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            products.append({"url": row["url"], "threshold": float(row["threshold"])} )
    return products

def get_price(url):
    try:
        page = requests.get(url, headers=HEADERS)
        print(page.text)  # DEBUG: Print the fetched HTML content
        soup = BeautifulSoup(page.content, "html.parser")
        price = None

        # Try various selectors for price
        selectors = [
            ('span', {'id': 'priceblock_ourprice'}),
            ('span', {'id': 'priceblock_dealprice'}),
            ('span', {'id': 'priceblock_saleprice'}),
            ('span', {'id': 'priceblock_businessprice'}),
            ('span', {'class': 'a-price-whole'}),
            ('span', {'class': 'a-offscreen'}),
        ]
        for tag, attrs in selectors:
            el = soup.find(tag, attrs=attrs)
            if el:
                price_str = el.get_text().replace(',', '').replace('₹', '').replace('$', '').strip()
                # Remove any non-numeric characters except dot
                price_str = re.sub(r'[^\d.]', '', price_str)
                try:
                    price = float(price_str)
                    break
                except ValueError:
                    continue
        return price
    except Exception as e:
        print(f"Error fetching price for {url}: {e}")
        return None

def log_price(url, price):
    with open("price_history.csv", "a", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([datetime.now().isoformat(), url, price])

def check_prices():
    products = read_products()
    for product in products:
        url = product["url"]
        threshold = product["threshold"]
        price = get_price(url)
        print(price)
        
        if price is not None:
            log_price(url, price)
            print(f"{url} - Current price: ${price} (Threshold: ${threshold})")
            if price < threshold:
                send_email_alert(url, price, threshold)
        else:
            print(f"Could not fetch price for {url}")

def main():
    try:
        with open("price_history.csv", "x", newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["timestamp", "url", "price"])
    except FileExistsError:
        pass

    schedule.every(10).seconds.do(check_prices)
    print("Amazon Price Tracker started. Press Ctrl+C to exit.")
    check_prices()
    while True:
        schedule.run_pending()
        time.sleep(10)

if __name__ == "__main__":
    main() 