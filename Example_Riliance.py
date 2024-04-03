from kiteconnect import KiteConnect
from threading import Thread
import time
import pandas as pd  # for calculating EMA

# Replace with your information
api_key = "YOUR_API_KEY"
access_token = "YOUR_ACCESS_TOKEN"
quantity = 1  # Adjust the quantity you want to buy

# Function to get instrument tokens
def get_instrument_tokens(symbols):
  kite = KiteConnect(api_key)
  instruments = kite.instruments("NSE")
  tokens = {}
  for instrument in instruments:
    if instrument["tradingsymbol"] in symbols:
      tokens[instrument["tradingsymbol"]] = instrument["instrument_token"]
  return tokens

# Function to calculate EMA for a given window
def calculate_ema(data, window):
  return data.ewm(span=window, adjust=False).mean()

# Function to place a buy order
def place_buy_order(token, quantity):
  kite = KiteConnect(api_key)
  try:
    order = kite.order_place(
        tradingsymbol=token.split("-")[0],  # Extract symbol from token
        exchange="NSE",
        transaction_type="BUY",
        quantity=quantity,
        product="CNC",
        order_type="MARKET"
    )
    if order["status"] == "failure":
      print("Order failed:", order["message"])
    else:
      print(f"Order placed for {token.split('-')[0]}:", order["order_id"])
  except Exception as e:
    print("Order placement error:", e)

# Main Script
symbols = ["RELIANCE", "NIFTY 50"]  # Instruments to monitor
instrument_tokens = get_instrument_tokens(symbols)
if not all(instrument_tokens.values()):
  missing_symbols = [symbol for symbol in symbols if symbol not in instrument_tokens]
  print(f"Instrument tokens not found for: {', '.join(missing_symbols)}")
  exit()

# Create a thread to continuously monitor live data
def monitor_ema():
  reliance_data = pd.DataFrame()
  nifty_data = pd.DataFrame()
  while True:
    # Get live data for Reliance and Nifty (modify if needed)
    try:
      historical_data = kite.historical_data(
          list(instrument_tokens.values()), from_date=datetime.datetime.now().strftime("%Y-%m-%d"), to_date=datetime.datetime.now().strftime("%Y-%m-%d"))
      for data in historical_data:
        symbol = data["tradingsymbol"]
        df = pd.DataFrame(data)
        if symbol == "RELIANCE":
          reliance_data = df
        elif symbol == "NIFTY 50":
          nifty_data = df
    except Exception as e:
      print("Error fetching live data:", e)
      time.sleep(5)  # Wait for 5 seconds before retrying

    if not (reliance_data.empty or nifty_data.empty):
      # Calculate EMAs for both Reliance and Nifty
      reliance_data["EMA_5"] = calculate_ema(reliance_data["close"], 5)
      reliance_data["EMA_13"] = calculate_ema(reliance_data["close"], 13)
      reliance_data["EMA_21"] = calculate_ema(reliance_data["close"], 21)

      nifty_data["EMA_5"] = calculate_ema(nifty_data["close"], 5)
      nifty_data["EMA_13"] = calculate_ema(nifty_data["close"], 13)
      nifty_data["EMA_21"] = calculate_ema(nifty_data["close"], 21)

      # Check for EMA crossover buy signal in both instruments
      reliance_buy_condition = (reliance_data.iloc[-1]["EMA_5"] > reliance_data.iloc[-1]["EMA_13"]) and (reliance_data.iloc[-1]["EMA_5"] > reliance_data.iloc[-1]["EMA_21"])
      nifty_buy_condition = (nifty_data.iloc[-1]["EMA_5"] > nifty_data.iloc[-1]["EMA_13"]) and (nifty_data.iloc[-1]["EMA_5"] > nifty_data.iloc[-1]["EMA_21"])

      # Buy only if both Reliance and Nifty meet