import kiteconnect
from kiteconnect import KiteConnect
import pyotp
from pyotp import TOTP
from kiteconnect import KiteTicker
import pandas as pd
import time
import datetime as dt


if __name__=='__main__':

    #autologin
    key_secret=open("api_key.txt",'r').read().split()
    kite=KiteConnect(api_key=key_secret[0])
    print(kite.login_url())

    request_token="MU8m1vDXTyDgJUYJHW5oY6fI6DZKbhXz"
    data=kite.generate_session(request_token,api_secret=key_secret[1])

    #create kite trading object
    kite.set_access_token(data["access_token"])
    #kite.set_access_token(access_token)
    print("kite session Generated ")
    print(kite.access_token)
