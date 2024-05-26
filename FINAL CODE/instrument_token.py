from kiteconnect import KiteConnect

# Initialize KiteConnect with your API key and access token
api_key = "gio34lqmlmn83a5"
access_token = "Y1Q63y8yQh7yBZO5d23fVkGPMG2u3bdM"
kite = KiteConnect(api_key=api_key)
kite.set_access_token(access_token)

def get_instrument_token(symbol, exchange):
    instruments = kite.instruments(exchange=exchange)
    for instrument in instruments:
        if instrument['tradingsymbol'] == symbol:
            return instrument['instrument_token']
    return None

# Example usage
symbol = "INFY"  # Example: Infosys
exchange = "NSE"  # Example: NSE
instrument_token = get_instrument_token(symbol, exchange)
if instrument_token:
    print(f"The instrument token for {symbol} on {exchange} is: {instrument_token}")
else:
    print("Instrument not found.")
from kiteconnect import KiteConnect

# Initialize KiteConnect with your API key and access token
# api_key = "gio34lqmlmn83a5"
# access_token = "m3eNQD3H1vLcpLYTPSOh4fIWTU8Nqdgu"
# kite = KiteConnect(api_key=api_key)
# kite.set_access_token(access_token)
#
#
# def get_instrument_tokens(exchange):
#     instruments = kite.instruments(exchange=exchange)
#     nifty_50_symbols = [
#         "ADANIPORTS", "ASIANPAINT", "AXISBANK", "BAJAJ-AUTO", "BAJAJFINSV",
#         "BAJFINANCE", "BHARTIARTL", "BPCL", "BRITANNIA", "CIPLA", "COALINDIA",
#         "DIVISLAB", "DRREDDY", "EICHERMOT", "GRASIM", "HCLTECH", "HDFC", "HDFCBANK",
#         "HDFCLIFE", "HEROMOTOCO", "HINDALCO", "HINDUNILVR", "ICICIBANK", "INDUSINDBK",
#         "INFY", "IOC", "ITC", "JSWSTEEL", "KOTAKBANK", "LT", "M&M", "MARUTI", "NESTLEIND",
#         "NTPC", "ONGC", "POWERGRID", "RELIANCE", "SBILIFE", "SBIN", "SHREECEM", "SUNPHARMA",
#         "TATAMOTORS", "TATASTEEL", "TCS", "TECHM", "TITAN", "ULTRACEMCO", "UPL", "WIPRO",
#         "DIVISLAB"
#     ]
#
#     nifty_50_instruments = []
#     for instrument in instruments:
#         if instrument['tradingsymbol'] in nifty_50_symbols:
#             nifty_50_instruments.append(instrument['instrument_token'])
#
#     return nifty_50_instruments
#
#
# # Example usage
# exchange = "NSE"
# nifty_50_instrument_tokens = get_instrument_tokens(exchange)
# print("Instrument Tokens for Nifty 50 Stocks:")
# print(nifty_50_instrument_tokens)
