import logging
import time
import pandas as pd
import numpy as np
import talib
from datetime import datetime, timedelta
from kiteconnect import KiteTicker, KiteConnect
import json

logging.basicConfig(level=logging.DEBUG)

# Initialise Kite Connect
kite = KiteConnect(api_key="5gio34lqmlmn83a5")
kite.set_access_token("cZshK8hJYGIsSqiXKoeZHuYs7Z85MsYg")

# Dictionary to store whether an order has been placed for an instrument token
order_placed = {}

# Dictionary to store historical data
historical_data_dict = {}

# List of instrument tokens to monitor
instrument_tokens = [738561]

# Nifty 50 instrument token (replace with the actual token for Nifty 50)
nifty_instrument_token = 256265

# Dictionary to store strike price difference and minimum quantity
strike_price_dict = {
    738561: {'strike_difference': 20, 'min_quantity': 250, 'symbol': 'RELIANCE', 'expiry': '24MAY'}

    # Example for Reliance
}

# Order file
order_file = "../MAY 24/orders.json"


def fetch_historical_data(instrument_token, days):
    today = pd.Timestamp.today().date()
    from_date = today - timedelta(days=days - 1)
    to_date = today
    historical_data = kite.historical_data(instrument_token, from_date, to_date, interval='day')
    df = pd.DataFrame(historical_data)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    return df


def fetch_last_price(instrument_token):
    last_price = kite.ltp(instrument_token)[str(instrument_token)]['last_price']
    return last_price


def calculate_ema(prices, period):
    prices_array = np.array(prices)
    return talib.EMA(prices_array, timeperiod=period)


def update_last_row(k, instrument_token):
    last_close = fetch_last_price(instrument_token)
    k.iloc[-1, k.columns.get_loc('close')] = last_close

    # Calculate EMAs for different periods
    k['5_day_ema'] = calculate_ema(k['close'], 5)
    k['13_day_ema'] = calculate_ema(k['close'], 13)


def buy_signal(instrument_token):
    # Fetch historical data if not already fetched
    if instrument_token not in historical_data_dict:
        historical_data_dict[instrument_token] = fetch_historical_data(instrument_token, days=84)

    # Fetch Nifty historical data if not already fetched
    if nifty_instrument_token not in historical_data_dict:
        historical_data_dict[nifty_instrument_token] = fetch_historical_data(nifty_instrument_token, days=84)

    # Fetch last traded price
    last_traded_price = fetch_last_price(instrument_token)

    # Update historical data with the last traded price
    update_last_row(historical_data_dict[instrument_token], instrument_token)
    update_last_row(historical_data_dict[nifty_instrument_token], nifty_instrument_token)

    # Check the condition for the stock
    ema_5 = historical_data_dict[instrument_token]['5_day_ema'].iloc[-1]
    ema_13 = historical_data_dict[instrument_token]['13_day_ema'].iloc[-1]

    if ema_5 > ema_13:
        return True, last_traded_price
    else:
        return False, last_traded_price


def sell_signal():
    # Read order details from the file
    try:
        with open(order_file, 'r') as file:
            orders = [json.loads(line) for line in file]
    except FileNotFoundError:
        orders = []

    signals = []
    for order in orders:
        instrument_token = order['instrument_token']
        if instrument_token not in historical_data_dict:
            historical_data_dict[instrument_token] = fetch_historical_data(instrument_token, days=84)

        # Update historical data with the last traded price
        update_last_row(historical_data_dict[instrument_token], instrument_token)

        ema_5 = historical_data_dict[instrument_token]['5_day_ema'].iloc[-1]
        ema_13 = historical_data_dict[instrument_token]['13_day_ema'].iloc[-1]

        if ema_5 < ema_13:
            signals.append(order)

    return signals


def calculate_atm_strike_price(last_traded_price, strike_difference):
    return round(last_traded_price / strike_difference) * strike_difference


def save_order_details(order_details):
    try:
        with open(order_file, 'a') as file:
            json.dump(order_details, file)
            file.write("\n")
        print("Order details saved to file.")
    except Exception as e:
        print(f"Error saving order details: {e}")


def remove_order_details(order_details):
    try:
        with open(order_file, 'r') as file:
            orders = [json.loads(line) for line in file]

        orders = [order for order in orders if order != order_details]

        with open(order_file, 'w') as file:
            for order in orders:
                json.dump(order, file)
                file.write("\n")
        print("Order details removed from file.")
    except Exception as e:
        print(f"Error removing order details: {e}")


def place_order(instrument_token, atm_strike_price, min_quantity, transaction_type):
    symbol = strike_price_dict[instrument_token]['symbol']
    expiry = strike_price_dict[instrument_token]['expiry']

    # Determine the put option strikes
    atm_put_trading_symbol = f"NFO:{symbol}{expiry}{atm_strike_price}PE"
    otm_put_strike_price = atm_strike_price - 2 * strike_price_dict[instrument_token]['strike_difference']
    otm_put_trading_symbol = f"NFO:{symbol}{expiry}{otm_put_strike_price}PE"

    try:
        if transaction_type == kite.TRANSACTION_TYPE_BUY:
            # Buy OTM put option
            ltp_data_otm_put = kite.ltp(otm_put_trading_symbol)[otm_put_trading_symbol]
            if 'last_price' in ltp_data_otm_put and ltp_data_otm_put['last_price'] is not None:
                market_price_otm_put = ltp_data_otm_put['last_price'] * 1.2
                kite.place_order(tradingsymbol=otm_put_trading_symbol[4:],
                                 exchange=kite.EXCHANGE_NFO,
                                 transaction_type=kite.TRANSACTION_TYPE_BUY,
                                 quantity=min_quantity,
                                 order_type=kite.ORDER_TYPE_LIMIT,
                                 price=round(market_price_otm_put, 1),
                                 variety=kite.VARIETY_REGULAR,
                                 product=kite.PRODUCT_NRML,
                                 validity=kite.VALIDITY_DAY)
                print(
                    f"Successfully placed buy order for {otm_put_trading_symbol} at market price: {market_price_otm_put}")

                # Save the order details
                order_details = {
                    'timestamp': str(datetime.now()),
                    'instrument_token': instrument_token,
                    'transaction_type': 'BUY',
                    'symbol': otm_put_trading_symbol,
                    'quantity': min_quantity,
                    'price': market_price_otm_put
                }
                save_order_details(order_details)
            else:
                print("Error: 'last_price' not found in market data for OTM put option")

        elif transaction_type == kite.TRANSACTION_TYPE_SELL:
            # Sell ATM put option
            ltp_data_atm_put = kite.ltp(atm_put_trading_symbol)[atm_put_trading_symbol]
            if 'last_price' in ltp_data_atm_put and ltp_data_atm_put['last_price'] is not None:
                market_price_atm_put = ltp_data_atm_put['last_price'] * 0.8
                kite.place_order(tradingsymbol=atm_put_trading_symbol[4:],
                                 exchange=kite.EXCHANGE_NFO,
                                 transaction_type=kite.TRANSACTION_TYPE_SELL,
                                 quantity=min_quantity,
                                 order_type=kite.ORDER_TYPE_LIMIT,
                                 price=round(market_price_atm_put, 1),
                                 variety=kite.VARIETY_REGULAR,
                                 product=kite.PRODUCT_NRML,
                                 validity=kite.VALIDITY_DAY)
                print(
                    f"Successfully placed sell order for {atm_put_trading_symbol} at market price: {market_price_atm_put}")

                # Save the order details
                order_details = {
                    'timestamp': str(datetime.now()),
                    'instrument_token': instrument_token,
                    'transaction_type': 'SELL',
                    'symbol': atm_put_trading_symbol,
                    'quantity': min_quantity,
                    'price': market_price_atm_put
                }
                save_order_details(order_details)
            else:
                print("Error: 'last_price' not found in market data for ATM put option")

    except Exception as e:
        print(f"Error placing {transaction_type} order: {e}")


def square_off_order(order_details):
    symbol = order_details['symbol']
    quantity = order_details['quantity']
    transaction_type = kite.TRANSACTION_TYPE_BUY if order_details[
                                                        'transaction_type'] == 'SELL' else kite.TRANSACTION_TYPE_SELL

    try:
        ltp_data = kite.ltp(symbol)[symbol]
        if 'last_price' in ltp_data and ltp_data['last_price'] is not None:
            if transaction_type == kite.TRANSACTION_TYPE_BUY:
                market_price = ltp_data['last_price'] * 1.2
            else:
                market_price = ltp_data['last_price'] * 0.8

            kite.place_order(tradingsymbol=symbol[4:],
                             exchange=kite.EXCHANGE_NFO,
                             transaction_type=transaction_type,
                             quantity=quantity,
                             order_type=kite.ORDER_TYPE_LIMIT,
                             price=round(market_price, 1),
                             variety=kite.VARIETY_REGULAR,
                             product=kite.PRODUCT_NRML,
                             validity=kite.VALIDITY_DAY)
            print(f"Successfully placed square off order for {symbol} at limit price: {market_price}")
        else:
            print(f"Error: 'last_price' not found in market data for {symbol}")
    except Exception as e:
        print(f"Error placing square off order for {symbol}: {e}")

def read_existing_orders():
    try:
        with open(order_file, 'r') as file:
            orders = [json.loads(line) for line in file]
        return orders
    except FileNotFoundError:
        return []

def check_existing_orders(instrument_token, atm_strike_price):
    for order in read_existing_orders():
        if order['instrument_token'] == instrument_token and order['symbol'] == f"NFO:{strike_price_dict[instrument_token]['symbol']}{strike_price_dict[instrument_token]['expiry']}{atm_strike_price}PE":
            return True
    return False

def on_ticks(ws, ticks):
    # Callback to receive ticks.
    for tick in ticks:
        last_price = tick['last_price']
        print("Last Traded Price:", last_price)

        instrument_token = tick['instrument_token']

        if instrument_token == nifty_instrument_token:
            # Nifty data is used only for comparison, not for trading
            continue

        # Check if the instrument_token exists in strike_price_dict
        if instrument_token in strike_price_dict:
            if instrument_token not in order_placed:
                # Check if similar orders exist in the order file
                atm_strike_price = calculate_atm_strike_price(last_price, strike_price_dict[instrument_token]['strike_difference'])
                if not check_existing_orders(instrument_token, atm_strike_price):
                    signal, last_traded_price = buy_signal(instrument_token)
                    if signal:
                        strike_difference = strike_price_dict[instrument_token]['strike_difference']
                        min_quantity = strike_price_dict[instrument_token]['min_quantity']
                        atm_strike_price = calculate_atm_strike_price(last_traded_price, strike_difference)

                        # Check if the order has already been placed for this token and strike price
                        if (instrument_token, atm_strike_price) not in order_placed:
                            place_order(instrument_token, atm_strike_price, min_quantity, kite.TRANSACTION_TYPE_SELL)
                            place_order(instrument_token, atm_strike_price, min_quantity, kite.TRANSACTION_TYPE_BUY)
                            order_placed[(instrument_token, atm_strike_price)] = True
                            print(
                                f"Buy Order Placed for Instrument Token: {instrument_token} at ATM strike price: {atm_strike_price}")
            else:
                # Check if we need to sell
                orders_to_square_off = sell_signal()
                for order in orders_to_square_off:
                    instrument_token = order['instrument_token']
                    square_off_order(order)
                    remove_order_details(order)
                    print(f"Sell Order Placed for Instrument Token: {instrument_token} at ATM strike price: {order['symbol']}")
        else:
            print(f"Instrument token {instrument_token} is not in strike_price_dict")






def on_connect(ws, response):
    # Callback on successful connect.
    # Subscribe to the list of instrument_tokens
    ws.subscribe(instrument_tokens + [nifty_instrument_token])


def on_close(ws, code, reason):
    # On connection close stop the main loop
    # Reconnection will not happen after executing `ws.stop()`
    ws.stop()


# Initialise WebSocket
kws = KiteTicker("5gio34lqmlmn83a5", "cZshK8hJYGIsSqiXKoeZHuYs7Z85MsYg")

# Assign the callbacks.
kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.on_close = on_close

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.
kws.connect()
