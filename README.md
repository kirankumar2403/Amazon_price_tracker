# Amazon Price Tracker

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Fill in your email details in `alert.py`.

3. Add product URLs and thresholds to `products.csv`.

4. Run the tracker:
   ```
   python tracker.py
   ```

## Notes

- The script checks prices every 6 hours by default.
- Alerts are sent via email when a price drops below your threshold.
- Price history is logged in `price_history.csv`. 