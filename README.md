# Amazon Price Tracker

A Flask web application that tracks Amazon product prices and sends email alerts when prices drop below your specified threshold.

## Features

- Web interface to add products and set price thresholds
- Automatic price tracking every 5 minutes
- Email alerts when prices drop
- Price history visualization
- Deployment-ready configuration

## Quick Start

### Option 1: Using the run script (Windows)
```bash
run.bat
```

### Option 2: Using the run script (Linux/Mac)
```bash
chmod +x run.sh
./run.sh
```

### Option 3: Manual setup
```bash
# Install dependencies
pip install -r requirements.txt

# Start the application
python app.py
```

## How it works

When you run `python app.py`, the application will:
1. Automatically create required CSV files (`products.csv` and `price_history.csv`)
2. Start the price tracker (`tracker.py`) in the background
3. Launch the Flask web server

## Configuration

### Email Alerts
Edit `alert.py` to configure your email settings:
- `EMAIL_ADDRESS`: Your Gmail address
- `EMAIL_PASSWORD`: Your Gmail app password
- `TO_EMAIL`: Recipient email address

### Deployment Settings
The app reads these environment variables for deployment:
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 5000)

Example for deployment:
```bash
export HOST=0.0.0.0
export PORT=8080
python app.py
```

## Usage

1. Open your browser and go to `http://localhost:5000`
2. Add Amazon product URLs and set price thresholds
3. The tracker will check prices every 5 minutes
4. You'll receive email alerts when prices drop below your threshold
5. View price history on the web interface

## File Structure

- `app.py` - Main Flask application (starts tracker automatically)
- `tracker.py` - Price tracking logic
- `alert.py` - Email notification system
- `templates/index.html` - Web interface
- `products.csv` - Product URLs and thresholds
- `price_history.csv` - Price tracking history
- `requirements.txt` - Python dependencies

## Deployment

This application is deployment-ready and can be deployed to:
- Heroku
- Railway
- PythonAnywhere
- Any VPS with Python support

The Flask app binds to `0.0.0.0` and reads PORT from environment variables for cloud deployment compatibility.
