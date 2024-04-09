from kiteconnect import KiteConnect
from datetime import datetime, timedelta

# Initialize KiteConnect with your API key and access token
api_key = "your_api_key"
access_token = "your_access_token"
kite = KiteConnect(api_key=api_key)
kite.set_access_token(access_token)


def get_reliance_current_month_expiry_token():
    # Fetch list of instruments for Reliance futures
    instruments = kite.instruments("NFO")

    # Get today's date
    today = datetime.today().date()

    # Iterate through instruments to find the desired contract
    for instrument in instruments:
        if "RELIANCE" in instrument['tradingsymbol'] and instrument['instrument_type'] == 'FUT':
            # Check if the expiry date is within the current month
            expiry_date = instrument['expiry']
            if expiry_date.year == today.year and expiry_date.month == today.month:
                return instrument['instrument_token']

# Get reliance current month expiry token
reliance_current_month_token = get_reliance_current_month_expiry_token()
print("Reliance current month expiry token:", reliance_current_month_token)

def get_reliance_next_month_expiry_token():
    # Fetch list of instruments for Reliance futures
    instruments = kite.instruments("NFO")

    # Get today's date and the first day of next month
    today = datetime.today().date()
    next_month = (today.replace(day=28) + timedelta(days=4)).replace(day=1)

    # Iterate through instruments to find the desired contract
    for instrument in instruments:
        if "RELIANCE" in instrument['tradingsymbol'] and instrument['instrument_type'] == 'FUT':
            # Check if the expiry date is within the next month
            expiry_date = instrument['expiry']
            if expiry_date.year == next_month.year and expiry_date.month == next_month.month:
                return instrument['instrument_token']

# Get reliance next month expiry token
reliance_next_month_token = get_reliance_next_month_expiry_token()
print("Reliance next month expiry token:", reliance_next_month_token)
