import time
import pandas as pd
from datetime import datetime, timedelta
from kiteconnect import KiteConnect

# # Initialize KiteConnect with your API key and access token
# api_key = 'your_api_key'
# access_token = 'your_access_token'
# kite = KiteConnect(api_key=api_key)
# kite.set_access_token(access_token)
#
# # Define instrument tokens for Nifty 50 index and Reliance stock
# nifty_token = 256265
# reliance_token = 738561

# Get historical data for Nifty 50 index for the past 10 days
today = datetime.today().date()
ten_days_ago = today - timedelta(days=10)

nifty_historical_data = kite.historical_data(instrument_token=nifty_token, from_date=ten_days_ago, to_date=today,
                                             interval='day')
reliance_historical_data = kite.historical_data(instrument_token=reliance_token, from_date=ten_days_ago, to_date=today,
                                                interval='day')

# Extract closing prices
nifty_closing_prices = [day['close'] for day in nifty_historical_data]
reliance_closing_prices = [day['close'] for day in reliance_historical_data]

# Initialize 5-day SMA and 10-day SMA for Nifty 50 index and Reliance stock
nifty_five_day_sma = sum(nifty_closing_prices[-5:]) / 5
nifty_ten_day_sma = sum(nifty_closing_prices) / 10

reliance_five_day_sma = sum(reliance_closing_prices[-5:]) / 5
reliance_ten_day_sma = sum(reliance_closing_prices) / 10

# Create a pandas DataFrame to store data
columns = ['Time', 'Nifty 5-Day SMA', 'Nifty 10-Day SMA', 'Reliance 5-Day SMA', 'Reliance 10-Day SMA']
data = pd.DataFrame(columns=columns)


# Function to calculate 5-day SMA
def calculate_sma5(prices):
    return sum(prices[-5:]) / 5


# Function to calculate 10-day SMA
def calculate_sma10(prices):
    return sum(prices) / 10


# Function to fetch and update current price
def fetch_update_price(instrument_token):
    current_price = kite.ltp(instrument_token=instrument_token)[str(instrument_token)]['last_price']
    return current_price


# Main loop to continuously calculate and store SMA every second
while True:
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Check if market is open (9:15 AM to 3:30 PM Indian Standard Time)
    if datetime.now().time() >= datetime.strptime('09:15:00','%H:%M:%S').time() and datetime.now().time() <= datetime.strptime('15:30:00', '%H:%M:%S').time():
        nifty_new_price = fetch_update_price(nifty_token)
        reliance_new_price = fetch_update_price(reliance_token)

        nifty_five_day_sma = calculate_sma5(nifty_closing_prices + [nifty_new_price])
        nifty_ten_day_sma = calculate_sma10(nifty_closing_prices + [nifty_new_price])

        reliance_five_day_sma = calculate_sma5(reliance_closing_prices + [reliance_new_price])
        reliance_ten_day_sma = calculate_sma10(reliance_closing_prices + [reliance_new_price])

        data = data.append({'Time': current_time,
                            'Nifty 5-Day SMA': nifty_five_day_sma,
                            'Nifty 10-Day SMA': nifty_ten_day_sma,
                            'Reliance 5-Day SMA': reliance_five_day_sma,
                            'Reliance 10-Day SMA': reliance_ten_day_sma}, ignore_index=True)

        print(
            f"Current Time: {current_time}, Nifty 5-Day SMA: {nifty_five_day_sma}, Nifty 10-Day SMA: {nifty_ten_day_sma}, Reliance 5-Day SMA: {reliance_five_day_sma}, Reliance 10-Day SMA: {reliance_ten_day_sma}")
    else:
        print("Market is closed.")
        break
    time.sleep(1)  # Wait for 1 second before checking again

# Save data to a CSV file
data.to_csv('sma_data_nifty_reliance.csv', index=False)
