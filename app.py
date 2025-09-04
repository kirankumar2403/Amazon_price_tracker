from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os
import subprocess
import sys

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

PRODUCTS_CSV = 'products.csv'
PRICE_HISTORY_CSV = 'price_history.csv'

def ensure_csv_files():
    """Ensure the CSV files exist with correct headers."""
    # Ensure products.csv has headers
    if not os.path.exists(PRODUCTS_CSV) or os.path.getsize(PRODUCTS_CSV) == 0:
        with open(PRODUCTS_CSV, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['url', 'threshold'])
    # Ensure price_history.csv has headers (tracker also handles this, but safe)
    if not os.path.exists(PRICE_HISTORY_CSV) or os.path.getsize(PRICE_HISTORY_CSV) == 0:
        with open(PRICE_HISTORY_CSV, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['timestamp', 'url', 'price'])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        threshold = request.form.get('threshold')
        if url and threshold:
            with open(PRODUCTS_CSV, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([url, threshold])
            flash('Product added successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Please provide both URL and threshold.', 'danger')
    # Read products
    products = []
    try:
        with open(PRODUCTS_CSV, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                products.append(row['url'])
    except FileNotFoundError:
        products = []
    # Read price history and group by product
    price_history_by_product = {url: [] for url in products}
    try:
        with open(PRICE_HISTORY_CSV, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                url = row['url']
                if url in price_history_by_product:
                    price_history_by_product[url].append(row)
    except FileNotFoundError:
        pass
    return render_template('index.html', price_history_by_product=price_history_by_product)

if __name__ == '__main__':
    # Prepare data files
    ensure_csv_files()
    # Start the tracker in the same terminal as a child process
    try:
        subprocess.Popen([sys.executable, 'tracker.py'], stdout=sys.stdout, stderr=sys.stderr)
    except Exception as e:
        print(f'Failed to start tracker.py: {e}')
    # Deployment-friendly server settings
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', '5000'))
    app.run(host=host, port=port, debug=False, use_reloader=False)
