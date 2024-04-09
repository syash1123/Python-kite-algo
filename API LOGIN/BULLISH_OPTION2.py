import time
from datetime import datetime, timedelta
from kiteconnect import KiteConnect
import calendar

# Initialize KiteConnect with your API key and access token
api_key = "5gio34lqmlmn83a5"
access_token = "5Q3OSkdIHaqhgVd1dgcwIdkDFVwVh8vg"
kite = KiteConnect(api_key=api_key)
kite.set_access_token(access_token)

# Define instrument tokens for Nifty 50 index and Reliance stock
nifty_token = 256265
reliance_token = 738561


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


# Function to place sell order for 1 put option of Reliance at given strike price
# # Function to place sell order for 1 put option of Reliance at given strike price
# # Function to place sell order for 1 put option of Reliance at given strike price
# def place_sell_put_order(strike_price, expiry_month):
#     tradingsymbol = f"RELIANCE24{expiry_month.upper()}{strike_price}PE"
#     print(f"Placing sell order for 1 put option of Reliance: {tradingsymbol}")
#     try:
#         kite.place_order(tradingsymbol=tradingsymbol,
#                          exchange=kite.EXCHANGE_NFO,
#                          transaction_type=kite.TRANSACTION_TYPE_SELL,
#                          quantity=1,
#                          order_type=kite.ORDER_TYPE_MARKET,
#                          variety=kite.VARIETY_REGULAR,
#                          product=kite.PRODUCT_MIS,
#                          validity=kite.VALIDITY_DAY)
#         print(f"Successfully placed sell order for 1 put option of Reliance: {tradingsymbol}")
#     except Exception as e:
#         print(f"Error placing sell order: {e}")


# Function to place buy order for 1 call option of Reliance at given strike price
# def place_sell_put_order(strike_price, expiry_month):
#     tradingsymbol = f"RELIANCE24{expiry_month.upper()}{strike_price}PE"
#     print(f"Placing sell order for 1 put option of Reliance: {tradingsymbol}")
#
#     try:
#         # Get market price of the option
#         market_price = kite.ltp(tradingsymbol)['last_price']
#
#         # Set limit price slightly above market price
#         limit_price = market_price * 1.0 # Adjust the multiplier as needed
#
#         # Place limit sell order
#         kite.place_order(tradingsymbol=tradingsymbol,
#                          exchange=kite.EXCHANGE_NFO,
#                          transaction_type=kite.TRANSACTION_TYPE_SELL,
#                          quantity=1,
#                          order_type=kite.ORDER_TYPE_LIMIT,
#                          price=limit_price,
#                          variety=kite.VARIETY_REGULAR,
#                          product=kite.PRODUCT_MIS,
#                          validity=kite.VALIDITY_DAY)
#
#         print(f"Successfully placed limit sell order for 1 put option of Reliance: {tradingsymbol}")
#     except Exception as e:
#         print(f"Error placing sell order: {e}")
def place_sell_put_order(strike_price, expiry_month):
    tradingsymbol = f"RELIANCE24{expiry_month.upper()}{strike_price}PE"
    print(f"Placing sell order for 1 put option of Reliance: {tradingsymbol}")

    try:
        # Retrieve market data for the option
        ltp_data = kite.ltp(tradingsymbol)

        # Check if 'last_price' is available in the market data
        if 'last_price' in ltp_data and ltp_data['last_price'] is not None:
            # Get last traded price of the option
            market_price = ltp_data['last_price']

            # Place limit sell order at market price
            kite.place_order(tradingsymbol=tradingsymbol,
                             exchange=kite.EXCHANGE_NFO,
                             transaction_type=kite.TRANSACTION_TYPE_SELL,
                             quantity=1,
                             order_type=kite.ORDER_TYPE_LIMIT,
                             price=market_price,
                             variety=kite.VARIETY_REGULAR,
                             product=kite.PRODUCT_MIS,
                             validity=kite.VALIDITY_DAY)

            print(f"Successfully placed limit sell order for 1 put option of Reliance at market price: {market_price}")
        else:
            print("Error: 'last_price' not found in market data")
    except Exception as e:
        print(f"Error placing sell order: {e}")


def place_buy_call_order(strike_price, expiry_month):
    tradingsymbol = f"RELIANCE{expiry_month.upper()}{strike_price}CE"
    print(f"Placing buy order for 1 call option of Reliance: {tradingsymbol}")
    # kite.place_order(tradingsymbol=tradingsymbol,
    #                  exchange=kite.EXCHANGE_NFO,
    #                  transaction_type=kite.TRANSACTION_TYPE_BUY,
    #                  quantity=1,
    #                  order_type=kite.ORDER_TYPE_MARKET,
    #                  variety=kite.VARIETY_REGULAR,
    #                  product=kite.PRODUCT_MIS,
    #                  validity=kite.VALIDITY_DAY)


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
        # Calculate the at-the-money (ATM) strike price for Reliance
        atm_strike = round(reliance_new_price / 20) * 20

        # Get the current month's name
        current_month_name = calendar.month_abbr[today.month]

        # Place sell order for 1 put option of Reliance at ATM strike price
        place_sell_put_order(atm_strike, current_month_name)
        print(f"Sell order placed for 1 put option of Reliance at strike price: {atm_strike}")

        # Place buy order for 1 call option of Reliance at ATM strike price - 2 * 20
        # place_buy_call_order(atm_strike - 2 * 20, current_month_name)
        # print(f"Buy order placed for 1 call option of Reliance at strike price: {atm_strike - 2 * 20}")

        break  # Exit loop after placing the orders

    time.sleep(1)  # Wait for 1 second before checking again
