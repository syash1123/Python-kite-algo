import time
from datetime import datetime, timedelta
from kiteconnect import KiteConnect


# Initialize KiteConnect with your API key and access token
api_key = "5gio34lqmlmn83a5"
access_token ="GADrNXTqhqJTVrursAZuMQJFfSbK7AO1"
kite = KiteConnect(api_key=api_key)
kite.set_access_token(access_token)

# Function to fetch instrument token for Reliance next month expiry contract
# def get_reliance_next_month_expiry_token():
#     # Fetch list of instruments for Reliance futures
#     instruments = kite.instruments("NSE")
#
#     # Get today's date and next month's date
#     today = datetime.today().date()
#     next_month = today.replace(day=28) + timedelta(days=4)  # Assuming next month has 31 days
#
#     # Find the instrument token for the next month expiry contract of Reliance
#     for instrument in instruments:
#         if instrument['tradingsymbol'] == 'RELIANCE' and datetime.strptime(instrument['expiry'], '%Y-%m-%d').date() == next_month:
#             return instrument['instrument_token']

# def get_reliance_current_month_expiry_token():
#     # Fetch list of instruments for Reliance futures
#     instruments = kite.instruments("NSE")
#
#     # Find the instrument token for the current month expiry contract of Reliance
#     for instrument in instruments:
#         if instrument['tradingsymbol'] == 'RELIANCE' and instrument['expiry'] == '2023-04-27':  # Update the expiry date as per the current month expiry
#             return instrument['instrument_token']

# def get_reliance_next_month_expiry_token():
#     # Fetch list of instruments for Reliance futures
#     instruments = kite.instruments("NSE")
#
#     # Get today's date and next month's date
#     today = datetime.today().date()
#     next_month = today.replace(day=28) + timedelta(days=4)  # Assuming next month has 31 days
#
#     # Find the instrument token for the next month expiry contract of Reliance
#     for instrument in instruments:
#         expiry_date = instrument.get('expiry')  # Get expiry date if it exists
#         if expiry_date and instrument['tradingsymbol'] == 'RELIANCE' and datetime.strptime(expiry_date, '%Y-%m-%d').date() == next_month:
#             return instrument['instrument_token']
#
# reliance_next_month = get_reliance_next_month_expiry_token()
# print(reliance_next_month)


from kiteconnect import KiteConnect
from datetime import datetime, timedelta

# Initialize KiteConnect with your API key and access token
api_key = "your_api_key"
access_token = "your_access_token"
kite = KiteConnect(api_key=api_key)
kite.set_access_token(access_token)

# def get_reliance_current_month_expiry_token():
#     # Fetch list of instruments for Reliance futures
#     instruments = kite.instruments("NSE")
#
#     # Get today's date
#     today = datetime.today().date()
#
#     # Find the instrument token for the current month expiry contract of Reliance
#     for instrument in instruments:
#         if instrument['tradingsymbol'] == 'RELIANCE' and instrument['instrument_type'] == 'FUT':
#             # Check if the expiry date is within the current month
#             expiry_date = datetime.strptime(instrument['expiry'], '%Y-%m-%d').date()
#             if expiry_date.year == today.year and expiry_date.month == today.month:
#                 return instrument['instrument_token']
#
# # Get reliance current month expiry token
# reliance_current_month_token = get_reliance_current_month_expiry_token()
# print("Reliance current month expiry token:", reliance_current_month_token)

from kiteconnect import KiteConnect
from datetime import datetime

# Initialize KiteConnect with your API key and access token
api_key = "your_api_key"
access_token = "your_access_token"
kite = KiteConnect(api_key=api_key)
kite.set_access_token(access_token)


from kiteconnect import KiteConnect
from datetime import datetime

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