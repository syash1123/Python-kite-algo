import threading
import time
from kiteconnect import KiteConnect

# Initialize Kite Connect
api_key = "your_api_key"
access_token = "your_access_token"
kite = KiteConnect(api_key=api_key)
kite.set_access_token(access_token)

# Function to fetch live data and calculate nearest ATM strike price
def get_nearest_strike_price():
    while True:
        # Fetch live data from Kite API (replace 'NSE:RELIANCE' with your desired instrument)
        ltp = kite.ltp('NSE:RELIANCE')['NSE:RELIANCE']['last_price']
        print("Live Price:", ltp)

        # Calculate nearest ATM strike price
        strike_price_difference = 50  # Change this value as needed
        atm_strike_price = ltp - (ltp % strike_price_difference)
        print("Nearest ATM Strike Price:", atm_strike_price)

        time.sleep(1)  # Fetch live data every second

# Main function to start fetching live data in a separate thread
def main():
    live_data_thread = threading.Thread(target=get_nearest_strike_price)
    live_data_thread.start()

if __name__ == "__main__":
    main()

# Keep the program running to continue fetching live data
