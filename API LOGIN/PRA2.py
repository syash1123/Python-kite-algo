from kiteconnect import KiteConnect
import datetime
import pandas as pd



# Initialize Kite Connect client with your API key and access token
api_key = "5gio34lqmlmn83a5"
access_token = "5Q3OSkdIHaqhgVd1dgcwIdkDFVwVh8vg"
kite = KiteConnect(api_key=api_key)
kite.set_access_token(access_token)

instruments=kite.instruments("NFO")
print(instruments)
instruments_df = pd.DataFrame(instruments)
# Save DataFrame to a CSV file
csv_file_path = 'instruments.csv'
instruments_df.to_csv(csv_file_path, index=False)

print(f"Instruments data saved to '{csv_file_path}'.")

# Convert DataFrame to Excel file
excel_file_path = 'instruments.xlsx'
instruments_df.to_excel(excel_file_path, index=False)




# # Define the instrument symbol for the option
# instrument_symbol = 'NFO:RELIANCE21APR2960PE'  # Change as per your requirement
#
# try:
#     # Fetch instrument details using the Kite Connect API
#     instrument_details = kite.ltp(instrument_symbol)
#
#     # Extract token number from the instrument details
#     token_number = instrument_details[instrument_symbol]['instrument_token']
#
#     print("Token Number:", token_number)
#
# except exceptions.TokenException as e:
#     print("TokenException:", e)
# except exceptions.GeneralException as e:
#     print("GeneralException:", e)
# except Exception as e:
#     print("An error occurred:", e)
#
# # Define the instrument symbol for the option
# instrument_symbol = 'NFO:RELIANCE21APR2960PE'  # Change as per your requirement
#
# try:
#     # Fetch instrument details using the Kite Connect API
#     instrument_details = kite.ltp(instrument_symbol)
#
#     # Extract token number from the instrument details
#     token_number = instrument_details[instrument_symbol]['instrument_token']
#
#     print("Token Number:", token_number)
#
# except exceptions.TokenException as e:
#     print("TokenException:", e)
# except exceptions.GeneralException as e:
#     print("GeneralException:", e)
# except Exception as e:
#     print("An error occurred:", e)

# # Define the instrument symbol for the option
# instrument_symbol = 'RELIANCE'
# expiry_date = datetime.date(2024, 4, 25)  # April 25, 2024
# strike_price = 2960
# option_type = 'CE'  # Call Option
#
# # Fetch instruments using Kite Connect API
# instruments = kite.instruments("NFO")
#
# # Filter instruments to find the specific option contract
# matching_instruments = [instrument for instrument in instruments if
#                        instrument['tradingsymbol'] == instrument_symbol
#                        and instrument['expiry'] == expiry_date
#                        and instrument['strike'] == strike_price
#                        and instrument['instrument_type'] == 'CE']
#
# if matching_instruments:
#     # Extract instrument token from the first matching instrument
#     option_token = matching_instruments[0]['instrument_token']
#     print("Option Token:", option_token)
# else:
#     print("Option not found.")

# # Define the search criteria
# symbol = 'RELIANCE'
# expiry = '2024-04-25'  # Expiry date in YYYY-MM-DD format
# strike_price = 2960
# option_type = 'CE'  # Call Option
#
# # Fetch instruments matching the search criteria
# instruments = kite.instruments('NFO')
# matching_instruments = [instrument for instrument in instruments if
#                         instrument['tradingsymbol'] == f'{symbol}{expiry}{strike_price}{option_type}']
#
# if matching_instruments:
#     # Extract instrument token from the first matching instrument
#     option_token = matching_instruments[0]['instrument_token']
#     print("Option Token:", option_token)
# else:
#     print("Option not found.")

# Define the search criteria
symbol = 'RELIANCE'
expiry = '2024-04-25'  # Expiry date in YYYY-MM-DD format
strike_price = 2960
option_type = 'CE'  # Call Option

# Construct the instrument symbol
instrument_symbol = f"{symbol}{expiry}{strike_price}{option_type}"

# Fetch instruments matching the search criteria
instruments = kite.instruments('NFO')
matching_instrument = next((instrument for instrument in instruments if instrument['tradingsymbol'] == instrument_symbol), None)

if matching_instrument:
    # Extract instrument token from the matching instrument
    option_token = matching_instrument['instrument_token']
    print("Option Token:", option_token)
else:
    print("Option not found.")