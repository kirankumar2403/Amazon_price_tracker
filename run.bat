@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo Starting Amazon Price Tracker...
python app.py

pause
