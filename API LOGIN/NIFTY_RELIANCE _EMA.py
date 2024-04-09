import time
from datetime import datetime, timedelta
from kiteconnect import KiteConnect

# Initialize KiteConnect with your API key and access token
api_key = 'your_api_key'
access_token = 'your_access_token'
kite = KiteConnect(api_key=api_key)
kite.set_access_token(access_token)

# Define instrument tokens for Nifty 50 index and Reliance stock
nifty_token = 256265
reliance_token = 738561


# Function to fetch and update current price
def fetch_update_price(instrument_token):
    current_price = kite.ltp(instrument_token=instrument_token)[str(instrument_token)]['last_price']
    return current_price


# Function to calculate simple moving average (SMA)
def calculate_sma(prices, period):
    return sum(prices[-period:]) / period


# Function to place buy order for 1 share of Reliance
def place_buy_order():
    kite.place_order(tradingsymbol='RELIANCE',
                     exchange=kite.EXCHANGE_NSE,
                     transaction_type=kite.TRANSACTION_TYPE_BUY,
                     quantity=1,
                     order_type=kite.ORDER_TYPE_MARKET,
                     variety=kite.VARIETY_REGULAR,
                     product=kite.PRODUCT_MIS)


# Main loop to continuously calculate and check SMA every second
while True:
    # Fetch current prices for Nifty and Reliance
    nifty_new_price = fetch_update_price(nifty_token)
    reliance_new_price = fetch_update_price(reliance_token)

    # Fetch historical data for Reliance for the past 10 days
    today = datetime.today().date()
    ten_days_ago = today - timedelta(days=10)
    reliance_historical_data = kite.historical_data(instrument_token=reliance_token, from_date=ten_days_ago,
                                                    to_date=today, interval='day')

    # Extract closing prices for Reliance
    reliance_closing_prices = [day['close'] for day in reliance_historical_data]

    # Calculate 5-day and 10-day simple moving averages (SMA) for Reliance
    reliance_five_day_sma = calculate_sma(reliance_closing_prices, 5)
    reliance_ten_day_sma = calculate_sma(reliance_closing_prices, 10)

    # Print current time and SMA values
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(
        f"Current Time: {current_time}, Reliance 5-Day SMA: {reliance_five_day_sma}, Reliance 10-Day SMA: {reliance_ten_day_sma}")

    # Check if 5-day SMA crosses 10-day SMA for both Nifty and Reliance
    if reliance_five_day_sma > reliance_ten_day_sma and nifty_five_day_sma > nifty_ten_day_sma:
        # Place buy order if conditions are met
        place_buy_order()
        print("Buy order placed for 1 Reliance share.")
        break  # Exit loop after placing the order

    time.sleep(1)  # Wait for 1 second before checking again
