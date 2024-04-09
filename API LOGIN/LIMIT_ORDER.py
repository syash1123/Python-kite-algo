def place_sell_put_order(strike_price, expiry_month):
    tradingsymbol = f"RELIANCE24{expiry_month.upper()}{strike_price}PE"
    print(f"Placing sell order for 1 put option of Reliance: {tradingsymbol}")

    try:
        # Get market price of the option
        market_price = kite.ltp(tradingsymbol)['last_price']

        # Set limit price slightly above market price
        limit_price = market_price * 1.01  # Adjust the multiplier as needed

        # Place limit sell order
        kite.place_order(tradingsymbol=tradingsymbol,
                         exchange=kite.EXCHANGE_NFO,
                         transaction_type=kite.TRANSACTION_TYPE_SELL,
                         quantity=1,
                         order_type=kite.ORDER_TYPE_LIMIT,
                         price=limit_price,
                         variety=kite.VARIETY_REGULAR,
                         product=kite.PRODUCT_MIS,
                         validity=kite.VALIDITY_DAY)

        print(f"Successfully placed limit sell order for 1 put option of Reliance: {tradingsymbol}")
    except Exception as e:
        print(f"Error placing sell order: {e}")