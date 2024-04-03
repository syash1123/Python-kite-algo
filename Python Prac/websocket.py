
from kiteconnect import WebSocket
import threading

# Initialize Kite WebSocket connection
api_key = 'your_api_key'
access_token = 'your_access_token'
kws = WebSocket(api_key=api_key, access_token=access_token)

# Define callbacks for WebSocket events
def on_ticks(ws, ticks):
    print("Ticks Update:", ticks)

def on_connect(ws, response):
    ws.subscribe(['NSE:SBIN'])  # Subscribe to tick updates for SBIN stock
    print("Connected to WebSocket")

def on_close(ws, code, reason):
    print("Connection closed:", code, reason)

# Assign callbacks to WebSocket events
kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.on_close = on_close

# Start WebSocket connection in a separate thread
def start_websocket():
    kws.connect(threaded=True)

# Start WebSocket connection
websocket_thread = threading.Thread(target=start_websocket)
websocket_thread.start()

# Keep the main thread running
while True:
    pass  # You can implement your logic here

# To gracefully close WebSocket connection, call:
# kws.close()
