from flask import Flask, render_template, request, redirect, url_for, flash
import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

PRODUCTS_CSV = 'products.csv'
PRICE_HISTORY_CSV = 'price_history.csv'

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
    with open(PRODUCTS_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            products.append(row['url'])
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
    app.run(debug=True)