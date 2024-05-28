from kiteconnect import KiteConnect
import json
from datetime import datetime

# Initialize Kite Connect
kite = KiteConnect(api_key="5gio34lqmlmn83a5")
kite.set_access_token("UN5NsQPfeO83bVAr4uxWxZeQ90jJHq4r")

order_file = "orders.json"

def fetch_live_positions():
    # Fetch live positions from Kite API
    return kite.positions()

def fetch_ltp(tradingsymbol):
    # Fetch the last traded price (LTP) for the given trading symbol
    ltp_data = kite.ltp(f"NFO:{tradingsymbol}")
    return ltp_data[f"NFO:{tradingsymbol}"]['last_price']

def square_off_position(position):
    tradingsymbol = position['tradingsymbol']
    exchange = position['exchange']
    quantity = abs(position['quantity'])
    product = position['product']

    if position['quantity'] > 0:
        # If the position is long, place a sell order to square off
        transaction_type = kite.TRANSACTION_TYPE_SELL
        ltp = fetch_ltp(tradingsymbol)
        limit_price = round(ltp * 0.8, 1)
    elif position['quantity'] < 0:
        # If the position is short, place a buy order to square off
        transaction_type = kite.TRANSACTION_TYPE_BUY
        ltp = fetch_ltp(tradingsymbol)
        limit_price = round(ltp * 1.2, 1)
    else:
        # No position to square off
        return

    try:
        # Place a limit order to square off the position
        kite.place_order(
            tradingsymbol=tradingsymbol,
            exchange=exchange,
            transaction_type=transaction_type,
            quantity=quantity,
            order_type=kite.ORDER_TYPE_LIMIT,
            price=limit_price,
            product=product,
            variety=kite.VARIETY_REGULAR
        )
        print(
            f"Successfully placed {transaction_type} order to square off {tradingsymbol} at limit price {limit_price}")

        # Update the order.json file to remove the squared-off position
        update_order_file(tradingsymbol)
    except Exception as e:
        print(f"Error placing order to square off {tradingsymbol}: {e}")

def update_order_file(tradingsymbol):
    try:
        with open(order_file, 'r') as file:
            orders = [json.loads(line) for line in file]

        updated_orders = [order for order in orders if order['symbol'] != f"NFO:{tradingsymbol}"]

        with open(order_file, 'w') as file:
            for order in updated_orders:
                json.dump(order, file)
                file.write("\n")
        print("Order file updated after squaring off position.")
    except Exception as e:
        print(f"Error updating order file: {e}")

def main():
    live_positions = fetch_live_positions()

    for position in live_positions['net']:
        square_off_position(position)

if __name__ == "__main__":
    main()
