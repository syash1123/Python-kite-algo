from kiteconnect import KiteConnect
from pyotp import TOTP
from kiteconnect import KiteTicker
import pandas as pd
import time
import datetime
from datetime import timedelta
import time
import pandas as pd
from datetime import datetime, timedelta
from kiteconnect import KiteConnect

kite=KiteConnect(api_key="5gio34lqmlmn83a5")
kite.set_access_token("8P1LtvJxNHV4e6JEVhIGECHsr4KLa472")
instrument_dump=kite.quote("NSE:SBIN")
print(instrument_dump)

today = datetime.today().date()
ten_days_ago = today - timedelta(days=10)

historical_data = kite.historical_data(instrument_token=738561, from_date=ten_days_ago, to_date=today, interval='day')


