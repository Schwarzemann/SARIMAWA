from flask import Flask, render_template, jsonify
import requests
import time
from threading import Thread
import pandas as pd
import csv
import logging

from fibonacci import fibonacci_retracement
from guesser import make_guess

app = Flask(__name__)
price_history = []
highest_price = float('-inf')
lowest_price = float('inf')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_real_time_data(symbol):
    url = f'https://www.okx.com/api/v5/market/ticker?instId={symbol}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            price = float(data['data'][0]['last'])
            return {'price': price}
        else:
            return {'error': f'Failed to fetch data. Status code: {response.status_code}'}
    except Exception as e:
        return {'error': f'An error occurred: {e}'}

def fetch_and_save_real_time_data(symbol):
    global price_history, highest_price, lowest_price
    while True:
        real_time_data = fetch_real_time_data(symbol)
        if 'price' in real_time_data:
            price = real_time_data['price']
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            entry = {'timestamp': timestamp, 'price': price}
            price_history.append(entry)
            highest_price = max(highest_price, price)
            lowest_price = min(lowest_price, price)
            fibonacci_levels = fibonacci_retracement(highest_price, lowest_price)
            # Save data to CSV
            with open('realtime_data.csv', 'w', newline='') as csvfile:
                fieldnames = ['timestamp', 'price']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for entry in price_history:
                    writer.writerow(entry)
        else:
            logger.error(f"Error: {real_time_data.get('error', 'Unknown error')}")
        time.sleep(5)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    global highest_price, lowest_price
    
    # Fetch real-time data
    symbol = 'BTC-USDT'
    real_time_data = fetch_real_time_data(symbol)
    if 'error' in real_time_data:
        return jsonify(real_time_data)

    price = real_time_data['price']
    price_history.append({'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'), 'price': price})

    # Update highest and lowest prices
    highest_price = max(highest_price, price)
    lowest_price = min(lowest_price, price)

    # Calculate Fibonacci retracement levels
    fibonacci_levels = fibonacci_retracement(highest_price, lowest_price)

    return jsonify({'price': price, 'fibonacci_levels': fibonacci_levels})

@app.route('/guess')
def get_guess():
    # Make a guess based on price history and Fibonacci levels
    next_price_guess, timestamp = make_guess()

    return jsonify({'guess': next_price_guess, 'timestamp': timestamp.isoformat()})

if __name__ == '__main__':
    # Start a separate thread to fetch and save real-time data
    symbol = 'BTC-USDT'
    data_fetch_thread = Thread(target=fetch_and_save_real_time_data, args=(symbol,))
    data_fetch_thread.start()

    # Run the Flask application
    app.run(debug=True)
