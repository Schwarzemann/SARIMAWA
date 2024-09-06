import requests
import time

def fetch_real_time_data(symbol):
    url = f'https://www.okx.com/api/v5/market/ticker?instId={symbol}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            price = float(data['data'][0]['last'])
            timestamp = time.strftime('%H:%M:%S')
            return {'timestamp': timestamp, 'price': price}
        else:
            return {'error': f'Failed to fetch data. Status code: {response.status_code}'}
    except Exception as e:
        return {'error': f'An error occurred: {e}'}

# Test the function
symbol = 'BTC-USDT'
data = fetch_real_time_data(symbol)
print(data)
