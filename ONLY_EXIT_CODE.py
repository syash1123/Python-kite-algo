import time
from datetime import datetime, timedelta
from kiteconnect import KiteConnect
import calendar

# Initialize KiteConnect with your API key and access token
api_key = "5gio34lqmlmn83a5"
access_token = "5B47CxMcJ2cAGab6jHfZ7iHrRWW465Rr"
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

def square_off_sell_put_order(strike_price, expiry_month):
    tradingsymbol = f"NFO:RELIANCE24{expiry_month.upper()}{strike_price}PE"
    print(f"Square off  sell order for 1 put option of Reliance: {tradingsymbol}")

    try:
        # Retrieve market data for the option
        ltp_data = kite.ltp(tradingsymbol)
        ltp_data=ltp_data[tradingsymbol]
        print(ltp_data)
        # Check if 'last_price' is available in the market data
        if 'last_price' in ltp_data and ltp_data['last_price'] is not None:
            # Get last traded price of the option
            market_price = ltp_data['last_price']*1.2
            print(market_price)
            # Place limit sell order at market price
            kite.place_order(tradingsymbol=tradingsymbol[4:],
                             exchange=kite.EXCHANGE_NFO,
                             transaction_type=kite.TRANSACTION_TYPE_BUY,
                             quantity=250,
                             order_type=kite.ORDER_TYPE_LIMIT,
                             price=round(market_price,1),
                             variety=kite.VARIETY_REGULAR,
                             product=kite.PRODUCT_MIS,
                             validity=kite.VALIDITY_DAY)

            # print({market_price})

            print(f"Successfully Squared off  sell order for 1 put option of Reliance at market price: {market_price}")
        else:
            print("Error: 'last_price' not found in market data")
    except Exception as e:
        print(f"Error placing sell order: {e}")

def square_off_call_order(strike_price, expiry_month):
    tradingsymbol = f"NFO:RELIANCE24{expiry_month.upper()}{strike_price}CE"
    print(f"Placing sell order for 1 call option of Reliance: {tradingsymbol}")

    try:
        # Retrieve market data for the option
        ltp_data = kite.ltp(tradingsymbol)
        ltp_data = ltp_data[tradingsymbol]
        print(ltp_data)
        # Check if 'last_price' is available in the market data
        if 'last_price' in ltp_data and ltp_data['last_price'] is not None:
            # Get last traded price of the option
            market_price = ltp_data['last_price'] * 0.8
            # print(market_price)
            # Place limit sell order at market price
            kite.place_order(tradingsymbol=tradingsymbol[4:],
                             exchange=kite.EXCHANGE_NFO,
                             transaction_type=kite.TRANSACTION_TYPE_SELL,
                             quantity=250,
                             order_type=kite.ORDER_TYPE_LIMIT,
                             price=round(market_price,1),
                             variety=kite.VARIETY_REGULAR,
                             product=kite.PRODUCT_MIS,
                             validity=kite.VALIDITY_DAY)

            # print({market_price})

            print(f"Successfully placed limit sell order for 1 put option of Reliance at market price: {market_price}")
        else:
            print("Error: 'last_price' not found in market data")
    except Exception as e:
        print(f"Error placing sell order: {e}")

def square_off_sell_fut_order(expiry_month):
    tradingsymbol = f"NFO:RELIANCE{expiry_month.upper()}FUT"
    print(f"Placing sell order for 1 lot of future : {tradingsymbol}")

    try:
        # Retrieve market data fot future
        ltp_data = kite.ltp(tradingsymbol)
        ltp_data = ltp_data[tradingsymbol]
        print(ltp_data)
        # Check if 'last_price' is available in the market data
        if 'last_price' in ltp_data and ltp_data['last_price'] is not None:
            # Get last traded price of the future
            market_price = ltp_data['last_price']
            # print(market_price)
            kite.place_order(tradingsymbol=tradingsymbol[4:],
                             exchange=kite.EXCHANGE_NFO,
                             transaction_type=kite.TRANSACTION_TYPE_SELL,
                             quantity=250,
                             order_type=kite.ORDER_TYPE_LIMIT,
                             price=round(market_price, 1),
                             variety=kite.VARIETY_REGULAR,
                             product=kite.PRODUCT_MIS,
                             validity=kite.VALIDITY_DAY)

            print(f"Successfully placed sell market  order for 1 lot of Reliance at market price: {market_price}")
        else:
            print("Error: 'last_price' not found in market data")
    except Exception as e:
        print(f"Error placing sell order: {e}")



#square off the position
while True:
    # Fetch current prices for Nifty and Reliance
    nifty_new_price = fetch_update_price(nifty_token)
    reliance_new_price = fetch_update_price(reliance_token)

    # Fetch historical data for Reliance for the past 21 days
    today = datetime.today().date()
    twenty_one_days_ago = today - timedelta(days=21)
    reliance_historical_data = kite.historical_data(instrument_token=reliance_token, from_date=twenty_one_days_ago,
                                                    to_date=today, interval='day')
    # Fetch historical data for Nifty for the past 21 days
    nifty_historical_data = kite.historical_data(instrument_token=nifty_token, from_date=twenty_one_days_ago,
                                                 to_date=today, interval='day')
    # Extract closing prices for Nifty
    nifty_closing_prices = [day['close'] for day in nifty_historical_data]

    # Calculate 5-day, 13-day, and 21-day exponential moving averages (EMA) for Nifty
    nifty_five_day_ema = calculate_ema(nifty_closing_prices, 5)
    nifty_thirteen_day_ema = calculate_ema(nifty_closing_prices, 13)
    nifty_twenty_one_day_ema = calculate_ema(nifty_closing_prices, 21)

    # Extract closing prices for Reliance
    reliance_closing_prices = [day['close'] for day in reliance_historical_data]

    # Calculate 5-day, 13-day, and 21-day exponential moving averages (EMA) for Reliance
    reliance_five_day_ema = calculate_ema(reliance_closing_prices, 5)
    reliance_thirteen_day_ema = calculate_ema(reliance_closing_prices, 13)
    reliance_twenty_one_day_ema = calculate_ema(reliance_closing_prices, 21)

    # Print current time and EMA values
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(
        f"Current Time: {current_time}, Reliance 5-Day EMA: {reliance_five_day_ema}, Reliance 13-Day EMA: {reliance_thirteen_day_ema}, Reliance 21-Day EMA: {reliance_twenty_one_day_ema}")
    print(
        f"Nifty 5-Day EMA: {nifty_five_day_ema}, Nifty 13-Day EMA: {nifty_thirteen_day_ema}, Nifty 21-Day EMA: {nifty_twenty_one_day_ema}")

    # Check if LTP for both becomes les both Nifty and Reliance
    if reliance_new_price <= reliance_thirteen_day_ema:

        # # Get the current month's name
        # current_month_name = calendar.month_abbr[today.month]
        #
        # # Place square off order for put option
        # square_off_sell_put_order(strike_price,expiry_month)
        # print(f" Square off Sell order placed for 1 put option of Reliance at strike price: {atm_strike}")
        #
        # #Place square off order for call option
        # square_off_call_order(strike_price=None, expiry_month=None)
        # print(f" Square off Buy order placed for 1 call option of Reliance at strike price: {atm_strike - 2 * 20}")
        #
        # #Place square off order for future
        # square_off_sell_fut_order(expiry_month=None)
        # print(f"Square off order placed for 1 Future lot of Reliance  for current month expiry.")

        break  # Exit loop after placing the orders

    time.sleep(1)  # Wait for 1 second before checking again













