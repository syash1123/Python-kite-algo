from kiteconnect import KiteConnect
from datetime import date, timedelta
import time

# Replace with your information
api_key = "YOUR_API_KEY"
access_token = "YOUR_ACCESS_TOKEN"

# Function to get instrument details (modify for your instrument)
def get_instrument_info(symbol, exchange="NSE"):
  kite = KiteConnect(api_key)
  instruments = kite.instruments(exchange)
  for instrument in instruments:
    if instrument["tradingsymbol"] == symbol:
      return instrument
  return None

# Function to place an order
def place_order(transaction_type, variety, exchange, symbol, quantity, price=None, product="CNC"):
  kite = KiteConnect(api_key)
  if price is None:
    order_type = "MARKET"
  else:
    order_type = "LIMIT"
  return kite.order_place(
      tradingsymbol=symbol,
      exchange=exchange,
      transaction_type=transaction_type,
      quantity=quantity,
      order_type=order_type,
      variety=variety,
      product=product,
      price=price
  )

# Main Script
today = date.today()
tomorrow = today + timedelta(days = 1)

# Get instrument information (replace with your symbol)
instrument = get_instrument_info("NIFTY")  # Modify instrument details

# Check if it's a future instrument and nearing expiry
if instrument and instrument["instrument_type"] == "FUT" and instrument["expiry"] == tomorrow.strftime("%Y-%m-%d"):
  # Sell current position
  order = place_order(
      transaction_type="SELL",
      variety=instrument["instrument_token"].split("-")[1],  # Assuming option type in token
      exchange=instrument["exchange"],
      symbol=instrument["tradingsymbol"],
      quantity=instrument["quantity"]
  )
  if order["status"] == "failure":
    print("Sell order failed:", order["message"])
  else:
    print("Sell order placed:", order["order_id"])

    # Get next month expiry details (logic needs improvement)
    next_month = today.month % 12 + 1  # Simplistic approach for next month
    next_expiry = f"{today.year}-{next_month:02d}-{instrument['expiry_day']}"

    # Buy next month contract (modify details as needed)
    order = place_order(
        transaction_type="BUY",
        variety=instrument["instrument_token"].split("-")[1],  # Assuming option type in token
        exchange=instrument["exchange"],
        symbol=instrument["tradingsymbol"],
        quantity=instrument["quantity"],
        expiry=next_expiry
    )
    if order["status"] == "failure":
      print("Buy order failed:", order["message"])
    else:
      print("Buy order placed:", order["order_id"])
else:
  print("Not a future or not near expiry")

# Add logic to handle errors and unexpected scenarios