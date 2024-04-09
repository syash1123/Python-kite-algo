import time
from datetime import datetime, timedelta
from kiteconnect import KiteConnect


# Initialize KiteConnect with your API key and access token
api_key = "5gio34lqmlmn83a5"
access_token ="GADrNXTqhqJTVrursAZuMQJFfSbK7AO1"
kite = KiteConnect(api_key=api_key)
kite.set_access_token(access_token)

# Define instrument tokens for Nifty 50 index and Reliance stock
nifty_token = 256265
reliance_token = 738561


# Function to fetch and update current price
# Function to fetch and update current price
def fetch_update_price(instrument_token):
    current_price = kite.ltp(instrument_token)[str(instrument_token)]['last_price']
    return current_price


# Function to calculate exponential moving average (EMA)
def calculate_ema(prices, period):
    alpha = 2 / (period + 1)
    ema = prices[0]
    for price in prices[1:]:
        ema = (1 - alpha) * ema + alpha * price
    return ema


# Function to place buy order for 1 share of Reliance
def place_buy_order():
    kite.place_order(tradingsymbol='RELIANCE',
                     exchange=kite.EXCHANGE_NSE,
                     transaction_type=kite.TRANSACTION_TYPE_BUY,
                     quantity=1,
                     order_type=kite.ORDER_TYPE_MARKET,
                     variety=kite.VARIETY_REGULAR,
                     product=kite.PRODUCT_MIS)


# Main loop to continuously calculate and check EMA every second
while True:
    # Fetch current prices for Nifty and Reliance
    nifty_new_price = fetch_update_price(nifty_token)
    reliance_new_price = fetch_update_price(reliance_token)

    # Fetch historical data for Reliance for the past 21 days
    today = datetime.today().date()
    twenty_one_days_ago = today - timedelta(days=21)
    reliance_historical_data = kite.historical_data(instrument_token=reliance_token, from_date=twenty_one_days_ago,
                                                    to_date=today, interval='day')

    # Extract closing prices for Reliance
    reliance_closing_prices = [day['close'] for day in reliance_historical_data]

    # Calculate 5-day, 13-day, and 21-day exponential moving averages (EMA) for Reliance
    reliance_five_day_ema = calculate_ema(reliance_closing_prices, 5)
    reliance_thirteen_day_ema = calculate_ema(reliance_closing_prices, 13)
    reliance_twenty_one_day_ema = calculate_ema(reliance_closing_prices, 21)

    # Fetch historical data for Nifty for the past 21 days
    nifty_historical_data = kite.historical_data(instrument_token=nifty_token, from_date=twenty_one_days_ago,
                                                 to_date=today, interval='day')

    # Extract closing prices for Nifty
    nifty_closing_prices = [day['close'] for day in nifty_historical_data]

    # Calculate 5-day, 13-day, and 21-day exponential moving averages (EMA) for Nifty
    nifty_five_day_ema = calculate_ema(nifty_closing_prices, 5)
    nifty_thirteen_day_ema = calculate_ema(nifty_closing_prices, 13)
    nifty_twenty_one_day_ema = calculate_ema(nifty_closing_prices, 21)

    # Print current time and EMA values
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(
        f"Current Time: {current_time}, Reliance 5-Day EMA: {reliance_five_day_ema}, Reliance 13-Day EMA: {reliance_thirteen_day_ema}, Reliance 21-Day EMA: {reliance_twenty_one_day_ema}")
    print(
        f"Nifty 5-Day EMA: {nifty_five_day_ema}, Nifty 13-Day EMA: {nifty_thirteen_day_ema}, Nifty 21-Day EMA: {nifty_twenty_one_day_ema}")

    # Check if 5-day EMA crosses both 13-day and 21-day EMA for both Nifty and Reliance
    if reliance_five_day_ema > reliance_thirteen_day_ema and reliance_five_day_ema > reliance_twenty_one_day_ema and \
            nifty_five_day_ema > nifty_thirteen_day_ema and nifty_five_day_ema > nifty_twenty_one_day_ema:
        # Place buy order if conditions are met
        # place_buy_order()
        # print("Buy order placed for 1 Reliance share.")
        break  # Exit loop after placing the order

    time.sleep(1)  # Wait for 1 second before checking again
