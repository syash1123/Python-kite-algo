import time
import pandas as pd
from datetime import datetime, timedelta
from kiteconnect import KiteConnect

# Initialize KiteConnect with your API key and access token
api_key = 'your_api_key'
access_token = 'your_access_token'
kite = KiteConnect(api_key=api_key)
kite.set_access_token(access_token)

# Get historical data for Reliance stock for the past 10 days
today = datetime.today().date()
ten_days_ago = today - timedelta(days=10)

historical_data = kite.historical_data(instrument_token=738561, from_date=ten_days_ago, to_date=today, interval='day')

# Extract closing prices
closing_prices = [day['close'] for day in historical_data]

# Initialize 5-day SMA and 10-day SMA
five_day_sma = sum(closing_prices[-5:]) / 5
ten_day_sma = sum(closing_prices) / 10

# Create a pandas DataFrame to store data
columns = ['Time', '5-Day SMA', '10-Day SMA']
data = pd.DataFrame(columns=columns)

# Function to calculate 5-day SMA
def calculate_sma5(new_price):
    nonlocal closing_prices
    closing_prices.pop(0)  # Remove oldest price
    closing_prices.append(new_price)  # Add new price
    return sum(closing_prices[-5:]) / 5

# Function to calculate 10-day SMA
def calculate_sma10(new_price):
    nonlocal closing_prices
    closing_prices.pop(0)  # Remove oldest price
    closing_prices.append(new_price)  # Add new price
    return sum(closing_prices) / 10

# Function to fetch and update current price
def fetch_update_price():
    current_price = kite.ltp(instrument_token=738561)['738561']['last_price']
    return current_price

# Main loop to continuously calculate and store SMA every second
while True:
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Check if market is open (9:15 AM to 3:30 PM Indian Standard Time)
    if datetime.now().time() >= datetime.strptime('09:15:00', '%H:%M:%S').time() and datetime.now().time() <= datetime.strptime('15:30:00', '%H:%M:%S').time():
        new_price = fetch_update_price()
        five_day_sma = calculate_sma5(new_price)
        ten_day_sma = calculate_sma10(new_price)
        data = data.append({'Time': current_time, '5-Day SMA': five_day_sma, '10-Day SMA': ten_day_sma}, ignore_index=True)
        print(f"Current Time: {current_time}, 5-Day SMA: {five_day_sma}, 10-Day SMA: {ten_day_sma}")
    else:
        print("Market is closed.")
        break
    time.sleep(1)  # Wait for 1 second before checking again

# Save data to a CSV file
data.to_csv('sma_data.csv', index=False)
