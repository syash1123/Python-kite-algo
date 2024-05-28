import logging
import json
from datetime import datetime
from kiteconnect import KiteConnect

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Initialise Kite Connect
kite = KiteConnect(api_key="5gio34lqmlmn83a5")
kite.set_access_token("JhEq7BUJ5nCWGRgFQntpvlV3ba7fxLFA")
# Strike price configuration
strike_price_dict = {
    341249: {'strike_difference': 10, 'min_quantity': 550, 'symbol': 'HDFCBANK', 'expiry': '24MAY'},
    738561: {'strike_difference': 20, 'min_quantity': 250, 'symbol': 'RELIANCE', 'expiry': '24MAY'}
}

# Order file
order_file = "orders.json"

def fetch_last_price(instrument_token):
    ltp = kite.ltp([instrument_token])
    return ltp[str(instrument_token)]['last_price']

def calculate_atm_strike_price(last_traded_price, strike_difference):
    return round(last_traded_price / strike_difference) * strike_difference

def square_off_position(tradingsymbol, transaction_type, quantity):
    try:
        ltp = fetch_last_price(tradingsymbol)
        if transaction_type == "BUY":
            limit_price = round(ltp * 0.8, 1)  # Set limit price for SELL order
            new_transaction_type = kite.TRANSACTION_TYPE_SELL
        elif transaction_type == "SELL":
            limit_price = round(ltp * 1.2, 1)  # Set limit price for BUY order
            new_transaction_type = kite.TRANSACTION_TYPE_BUY

        kite.place_order(
            tradingsymbol=tradingsymbol[4:],
            exchange="NFO",
            transaction_type=new_transaction_type,
            quantity=quantity,
            order_type=kite.ORDER_TYPE_LIMIT,
            price=limit_price,
            product=kite.PRODUCT_NRML,
            variety=kite.VARIETY_REGULAR
        )
        logging.info(f"Successfully placed {new_transaction_type} order for {tradingsymbol} at limit price {limit_price}")
    except Exception as e:
        logging.error(f"Error placing order for {tradingsymbol}: {e}")

def place_order(instrument_token, strike_price, min_quantity, transaction_type, strike_type):
    symbol = strike_price_dict[instrument_token]['symbol']
    expiry = strike_price_dict[instrument_token]['expiry']
    strike_difference = strike_price_dict[instrument_token]['strike_difference']
    trading_symbol = f"NFO:{symbol}{expiry}{strike_price}PE" if strike_type == 'ATM' else f"NFO:{symbol}{expiry}{strike_price - 2 * strike_difference}PE"

    last_price = fetch_last_price(instrument_token)
    limit_price = round(last_price * (0.8 if transaction_type == kite.TRANSACTION_TYPE_SELL else 1.2), 1)

    try:
        kite.place_order(
            tradingsymbol=trading_symbol[4:],
            exchange=kite.EXCHANGE_NFO,
            transaction_type=transaction_type,
            quantity=min_quantity,
            order_type=kite.ORDER_TYPE_LIMIT,
            price=limit_price,
            variety=kite.VARIETY_REGULAR,
            product=kite.PRODUCT_NRML,
            validity=kite.VALIDITY_DAY
        )

        order_details = {
            'timestamp': str(datetime.now()),
            'instrument_token': instrument_token,
            'transaction_type': transaction_type,
            'symbol': trading_symbol,
            'quantity': min_quantity,
            'price': limit_price,
            'strike_price': strike_price,
            'strike_type': strike_type
        }
        return order_details
    except Exception as e:
        logging.error(f"Error placing {transaction_type} order: {e}")
        return None

def process_orders():
    with open(order_file, 'r') as file:
        orders = [json.loads(line) for line in file if line.strip()]

    updated_orders = []

    for order in orders:
        instrument_token = order['instrument_token']
        if instrument_token not in strike_price_dict:
            continue

        last_price = fetch_last_price(instrument_token)
        strike_difference = strike_price_dict[instrument_token]['strike_difference']
        min_quantity = strike_price_dict[instrument_token]['min_quantity']

        current_atm_strike_price = calculate_atm_strike_price(last_price, strike_difference)
        current_otm_strike_price = current_atm_strike_price - 2 * strike_difference

        if order['strike_type'] == 'ATM' and order['strike_price'] != current_atm_strike_price:
            square_off_position(order['symbol'], order['transaction_type'], order['quantity'])
            new_order = place_order(instrument_token, current_atm_strike_price, min_quantity, order['transaction_type'], 'ATM')
            if new_order:
                updated_orders.append(new_order)
        elif order['strike_type'] == 'OTM' and order['strike_price'] != current_otm_strike_price:
            square_off_position(order['symbol'], order['transaction_type'], order['quantity'])
            new_order = place_order(instrument_token, current_otm_strike_price, min_quantity, order['transaction_type'], 'OTM')
            if new_order:
                updated_orders.append(new_order)
        else:
            updated_orders.append(order)

    with open(order_file, 'w') as file:
        for order in updated_orders:
            json.dump(order, file)
            file.write("\n")

# Start processing orders
process_orders()
