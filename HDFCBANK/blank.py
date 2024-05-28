import logging
import time
import pandas as pd
import numpy as np
import talib
from datetime import datetime, timedelta
from kiteconnect import KiteTicker, KiteConnect
import json
import os
import json

# Get the current directory
current_directory = os.getcwd()
print(current_directory)

# Construct the file path for the order file
order_file = os.path.join(current_directory, "orders.json")
print(order_file)
with open(order_file, 'r') as file:
            print('opening file')
            orders = [json.loads(line) for line in file]
            print(orders)

def read_existing_orders():
    print('hell')
    try:
        print('reading existing orders')
        with open(order_file, 'r') as file:
            print('opening file')
            orders = [json.loads(line) for line in file]
            print(orders)
        return orders
    except FileNotFoundError:
        return []

print(5)

print(read_existing_orders())