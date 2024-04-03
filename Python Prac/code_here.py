from kite_trade import *
import pandas as pd
import numpy as np
from datetime import *
import json
from constants import cols, file_path
from utilities import write_to_csv

enctoken = "hpP78CB4FHJEtZDLLoXKE6d+i4KLaz8gio3pKYsCy/zGk40iHTxevWzH4JYUN/zXDlKpiF5REpdC6WDLyydfrjpO8QJIc7GtyUu42QDHraTdK2iQ+CT/+w=="
kite = KiteApp(enctoken=enctoken)


print((kite.margins()))

stock='NSE:SBIN'
data=kite.quote([stock])[stock]
print(data)
write_to_csv(data, file_path, cols)

print()

# import time
# while True:
#     data = kite.quote(["NSE:SBIN"])
#     new_df = pd.DataFrame([data])
#     df = df._append(new_df, ignore_index=True)
#     print(df)
#     time.sleep(1)

# new_order=kite.place_order(variety=kite.VARIETY_REGULAR,
#                            exchange=kite.EXCHANGE_NSE,
#                            tradingsymbol="SBIN",
#                            transaction_type=kite.TRANSACTION_TYPE_BUY,
#                            order_type=kite.ORDER_TYPE_MARKET,
#                            quantity=1,
#                            product=kite.ORDER_TYPE_LIMIT,
#                            price=None,
#                            validity=None,
#                            disclosed_quantity=None,
#                            trigger_price=None,
#                            squareoff=None,
#                            stoploss=None,
#                            trailing_stoploss=None,
#                            tag=None)
#
# print(new_order)




# order = kite.place_order(variety=kite.VARIETY_REGULAR,
#                        exchange=kite.EXCHANGE_NSE,
#                        tradingsymbol="SBIN",
#                        transaction_type=kite.TRANSACTION_TYPE_BUY,
#                        quantity=1,
#                        product=kite.PRODUCT_MIS,
#                        order_type=kite.ORDER_TYPE_LIMIT,
#                        price=None,
#                        validity=None,
#                        disclosed_quantity=None,
#                        trigger_price=None,
#                        squareoff=None,
#                        stoploss=None,
#                        trailing_stoploss=None,
#                        tag="TradeViaPython")
#
# print(order)