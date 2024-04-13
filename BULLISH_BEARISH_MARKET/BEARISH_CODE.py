import time
from datetime import datetime,timedelta
from kiteconnect import KiteConnect
import calendar

# Initialize KiteConnect with your API key and access token
api_key = "5gio34lqmlmn83a5"
access_token = "bhHdFLqVppg6NDYUA3jj35upGbDU7uvE"
kite = KiteConnect(api_key=api_key)
kite.set_access_token(access_token)

# Define instrument tokens for Nifty 50 index and Reliance stock
nifty_token = 256265
reliance_token = 738561

# Function to fetch update current price
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

# Function to calculate the sell call optionn of ATM strike
def place_sell_call_order(strike_price,expiry_month):
    tradingsymbol = f"NFO:RELIANCE24{expiry_month}{strike_price}CE"
    print(f"Placing sell order for 1 call of Reliance : {tradingsymbol}")

    try:
        #Retreive market data of option
        ltp_data = kite.ltp(tradingsymbol)
        ltp_data = ltp_data[tradingsymbol]
        print(ltp_data)
    # Check if 'last_price' is available in the market data
        if 'last_price' in ltp_data and ltp_data['last_price'] is not None:
            # Get last traded price of the option
            market_price = ltp_data['last_price']*0.8
            print(market_price)
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

            print(f"Successfully placed limit sell order for 1 Call option of Reliance at market price: {market_price}")
        else:
            print("Error: 'last_price' not found in market data")
    except Exception as e:
        print(f"Error placing sell order: {e}")


# Function to place a buy order for put option.
def place_buy_pe_order(strike_price,expiry_month):
    tradingsymbol = f"NFO:RELIANCE24{expiry_month.upper()}{strike_price}CE"
    print(f"Placing buy order for 1 lot of PE option of Reliance : {tradingsymbol}")

    try:
        # Retrieve market data for the option
        ltp_data = kite.ltp(tradingsymbol)
        ltp_data = ltp_data[tradingsymbol]
        print(ltp_data)
        # Check if 'last_price' is available in the market data
        if 'last_price' in ltp_data and ltp_data['last_price'] is not None:
            # Get last traded price of the option
            market_price = ltp_data['last_price'] * 1.02
            # print(market_price)
            # Place limit sell order at market price
            kite.place_order(tradingsymbol=tradingsymbol[4:],
                             exchange=kite.EXCHANGE_NFO,
                             transaction_type=kite.TRANSACTION_TYPE_BUY,
                             quantity=250,
                             order_type=kite.ORDER_TYPE_LIMIT,
                             price=round(market_price, 1),
                             variety=kite.VARIETY_REGULAR,
                             product=kite.PRODUCT_MIS,
                             validity=kite.VALIDITY_DAY)

            # print({market_price})

            print(f"Successfully placed limit buy  order for 1 put option of Reliance at market price: {market_price}")
        else:
            print("Error: 'last_price' not found in market data")
    except Exception as e:
        print(f"Error placing sell order: {e}")


# Function to place a sell order for the future .
def place_sell_fut_order(expiry_month):
    tradingsymbol = f"NFO:RELIANCE24{expiry_month.upper()}FUT"
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

            print(f"Successfully placed sell market  order for 1 lot of future Reliance at market price: {market_price}")
        else:
            print("Error: 'last_price' not found in market data")
    except Exception as e:
        print(f"Error placing sell order: {e}")

#Function to square off sell all order
def square_off_sell_call_order(strike_price,expiry_month):
    tradingsymbol = f"NFO:RELIANCE24{expiry_month}{strike_price}CE"
    print(f"Square off  sell order for 1 call of Reliance : {tradingsymbol}")

    try:
        #Retreive market data of option
        ltp_data = kite.ltp(tradingsymbol)
        ltp_data = ltp_data[tradingsymbol]
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

            print(f"Successfully Squared off limit sell order for 1 Call option of Reliance at market price: {market_price}")
        else:
            print("Error: 'last_price' not found in market data")
    except Exception as e:
        print(f"Error placing sell order: {e}")

# Function to Square off Buy PE order
def Square_off_buy_pe_order(strike_price,expiry_month):
    tradingsymbol = f"NFO:RELIANCE24{expiry_month.upper()}{strike_price}CE"
    print(f"Square off  buy order for 1 lot of PE option of Reliance : {tradingsymbol}")

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
                             price=round(market_price, 1),
                             variety=kite.VARIETY_REGULAR,
                             product=kite.PRODUCT_MIS,
                             validity=kite.VALIDITY_DAY)

            # print({market_price})

            print(f"Successfully squared off  limit order buy  order for 1 put option of Reliance at market price: {market_price}")
        else:
            print("Error: 'last_price' not found in market data")
    except Exception as e:
        print(f"Error placing sell order: {e}")

#Function to square off Future order.
def Square_off_sell_fut_order(expiry_month):
    tradingsymbol = f"NFO:RELIANCE24{expiry_month.upper()}FUT"
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
                             transaction_type=kite.TRANSACTION_TYPE_BUY,
                             quantity=250,
                             order_type=kite.ORDER_TYPE_LIMIT,
                             price=round(market_price, 1),
                             variety=kite.VARIETY_REGULAR,
                             product=kite.PRODUCT_MIS,
                             validity=kite.VALIDITY_DAY)

            print(f"Successfully Squared off  sell market  order for 1 lot of future Reliance at market price: {market_price}")
        else:
            print("Error: 'last_price' not found in market data")
    except Exception as e:
        print(f"Error placing sell order: {e}")






atm_strike = None #read from text file
count = 0 # read from txt file
#Main loop to countinously calculate and check EMA every second

while count == 0:
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


    if reliance_five_day_ema<=reliance_thirteen_day_ema and reliance_thirteen_day_ema <=reliance_twenty_one_day_ema and nifty_five_day_ema<=nifty_thirteen_day_ema and nifty_thirteen_day_ema<=nifty_twenty_one_day_ema:


        # Calculate the at-the-money (ATM) strike price for Reliance
        atm_strike = round(reliance_new_price / 20) * 20

        # Get the current month's name
        current_month_name = calendar.month_abbr[today.month]

        #Placing sell order for call option for 1 lot of Reliace at ATM strike price
        place_sell_call_order(atm_strike,current_month_name)
        print(f"Sell order placed for 1 call option of Reliance at strike price : {atm_strike}")

        #Placing buy order for put option for 1 lot of Reliance at ATM strike + 2*20
        place_buy_pe_order(atm_strike + 2*20,current_month_name)
        print(f"Buy  order placed for 1 put option of Reliance at strike price : {atm_strike + 2*20}")

        #Placing sell order for Future of Reliance for current month.
        place_sell_fut_order(current_month_name)
        print(f"Sell order placed for 1 lot of future reliance for current month expiry .")


        count += 1
        #put to txt
        break  #exit loop after placing the order

    time.sleep(1) #wait for 1 sec before placing the order.


   #----------------------------------------------------------------------------SQUARE OFF CODE --------------------------------------------------------------------------#
#square off the positons code
#GET COUNT FROM TXT

while count :
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

    if reliance_new_price >= reliance_thirteen_day_ema or nifty_new_price >= nifty_thirteen_day_ema:
        # Current the at the money (ATM) strike for Reliance
        # atm_strike = round(reliance_new_price/20)*20

        #Get the current months name
        current_month_name = calendar.month_abbr[today.month]

        #Place square off order for sell call order
        square_off_sell_call_order(atm_strike,expiry_month=current_month_name)
        print(f"Sucessfully squared off call order for atm strikr : {atm_strike}")

        #Place square off order for Buy PE order
        Square_off_buy_pe_order(atm_strike,current_month_name)
        print(f"Sucessfully squared off PE buy order for atm strike :{atm_strike + 2*20}")


        #Place square off for Future order
        Square_off_sell_fut_order(current_month_name)
        print(f"Sucessfully squared off Future order ")

        count -= 1

        break    # Exit loop after placing the orders

    time.sleep(1)   # Wait for 1 second before checking again


#save count & atm_strike both to the same file txt file at the end of the day

#GO TO FUNCTION IN PYTHON

#------------------------------------------------END OF CODE --------------------------------------------------#
















