# import json
# import pandas as pd
# from kiteconnect import KiteConnect
# from datetime import datetime, timedelta
#
# # Initialize Kite Connect
# api_key = "5gio34lqmlmn83a5"
# access_token = "zxLUTBvFc74orxsolSlaaSnHjRQkNYNU"
# kite = KiteConnect(api_key=api_key)
# kite.set_access_token(access_token)
#
#
# # Function to fetch historical data
# def fetch_historical_data(instrument_token, days):
#     """Fetch historical data for the given instrument token"""
#     end_date = datetime.now()
#     start_date = end_date - timedelta(days=days)
#     interval = "day"
#
#     data = kite.historical_data(instrument_token, start_date, end_date, interval)
#     return pd.DataFrame(data)
#
#
# # Function to calculate EMA
# def calculate_ema(df, span):
#     """Calculate the Exponential Moving Average (EMA)"""
#     return df['close'].ewm(span=span, adjust=False).mean()
#
#
# # Function to square off position
# def square_off_position(tradingsymbol, transaction_type, quantity):
#     """Square off a position by placing an opposite limit order"""
#     ltp = kite.ltp(tradingsymbol)[tradingsymbol]['last_price']
#     if transaction_type == "BUY":
#         limit_price = round(ltp * 0.8, 1)  # Set limit price for SELL order
#         new_transaction_type = "SELL"
#     elif transaction_type == "SELL":
#         limit_price = round(ltp * 1.2, 1)  # Set limit price for BUY order
#         new_transaction_type = "BUY"
#
#     try:
#         kite.place_order(
#             tradingsymbol=tradingsymbol,
#             exchange="NFO",
#             transaction_type=new_transaction_type,
#             quantity=quantity,
#             order_type=kite.ORDER_TYPE_LIMIT,
#             price=limit_price,
#             product=kite.PRODUCT_MIS,
#             variety=kite.VARIETY_REGULAR
#         )
#         print(f"Successfully placed {new_transaction_type} order for {tradingsymbol} at limit price {limit_price}")
#     except Exception as e:
#         print(f"Error placing order for {tradingsymbol}: {e}")
#
#
# # Main function to process orders
# def process_orders():
#     with open("orders.json", "r") as file:
#         lines = file.readlines()
#
#     for line in lines:
#         order = json.loads(line)
#         instrument_token = order['instrument_token']
#         tradingsymbol = order['symbol']
#         transaction_type = order['transaction_type']
#         quantity = order['quantity']
#
#         # Fetch historical data
#         df = fetch_historical_data(instrument_token, 20)
#
#         # Calculate 5-day and 13-day EMA
#         df['ema_5'] = calculate_ema(df, 5)
#         df['ema_13'] = calculate_ema(df, 13)
#
#         # Check if the 5-day EMA is greater than the 13-day EMA
#         if df['ema_5'].iloc[-1] > df['ema_13'].iloc[-1]:
#             # Square off the position
#             square_off_position(tradingsymbol, transaction_type, quantity)
# if __name__ == "__main__":
#     process_orders()

import json
import logging

import pandas as pd
from kiteconnect import KiteConnect
from datetime import datetime, timedelta

logging.basicConfig(level=logging.DEBUG)
# Initialize Kite Connect
api_key = "5gio34lqmlmn83a5"
access_token = "cZshK8hJYGIsSqiXKoeZHuYs7Z85MsYg"
kite = KiteConnect(api_key=api_key, debug=True)

kite.set_access_token(access_token)

# Function to fetch historical data
def fetch_historical_data(instrument_token, days):
    """Fetch historical data for the given instrument token"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    interval = "day"

    data = kite.historical_data(instrument_token, start_date, end_date, interval)
    return pd.DataFrame(data)

# Function to calculate EMA
def calculate_ema(df, span):
    """Calculate the Exponential Moving Average (EMA)"""
    return df['close'].ewm(span=span, adjust=False).mean()

# Function to check if an instrument is valid
def is_valid_instrument(tradingsymbol):
    """Check if the instrument exists and is valid"""
    try:
        kite.ltp(tradingsymbol)
        return True
    except Exception as e:
        print(f"Invalid instrument: {tradingsymbol}, error: {e}")
        return False

# Function to square off position
def square_off_position(tradingsymbol, transaction_type, quantity):
    """Square off a position by placing an opposite limit order"""

    try:
        ltp = kite.ltp(tradingsymbol)[tradingsymbol]['last_price']
        new_transaction_type=""
        limit_price=0
        if transaction_type == "BUY":
            limit_price = round(ltp * 0.8, 1)  # Set limit price for SELL order
            new_transaction_type = kite.TRANSACTION_TYPE_SELL
        elif transaction_type == "SELL":
            limit_price = round(ltp * 1.2, 1)  # Set limit price for BUY order
            new_transaction_type = kite.TRANSACTION_TYPE_BUY

        kite.place_order(
            tradingsymbol=tradingsymbol,
            exchange="NFO",
            transaction_type=new_transaction_type,
            quantity=quantity,
            order_type=kite.ORDER_TYPE_LIMIT,
            price=limit_price,
            product=kite.PRODUCT_NRML,
            variety=kite.VARIETY_REGULAR
        )
        print(f"Successfully placed {new_transaction_type} order for {tradingsymbol} at limit price {limit_price}")
    except Exception as e:
        print(f"Error placing order for {tradingsymbol}: {e}")

# Main function to process orders
def process_orders():
    with open("../MAY 24/orders.json", "r") as file:
        lines = file.readlines()

    for line in lines:
        order = json.loads(line)
        instrument_token = order['instrument_token']
        tradingsymbol = order['symbol'][4:]
        transaction_type = order['transaction_type']
        quantity = order['quantity']



        # Check if the instrument is valid
        if not is_valid_instrument(tradingsymbol):
            print(f"Skipping invalid instrument: {tradingsymbol}")
            continue

        # Fetch historical data
        df = fetch_historical_data(instrument_token, 84)

        # Calculate 5-day and 13-day EMA
        df['ema_5'] = calculate_ema(df, 5)
        df['ema_13'] = calculate_ema(df, 13)



        # Check if the 5-day EMA is greater than the 13-day EMA
        # if df['ema_5'].iloc[-1] > df['ema_13'].iloc[-1]:
        #     # Square off the position
        square_off_position(tradingsymbol, transaction_type, quantity)

if __name__ == "__main__":
    process_orders()
