import time

import numpy as np

import RSI

APCA_API_SECRET_KEY = ''  # Enter Your Secret Key Here
APCA_API_KEY_ID = ''  # Enter Your Public Key Here
APCA_API_BASE_URL = 'https://paper-api.alpaca.markets'  # This is the base URL for paper trading
api = tradeapi.REST(key_id=APCA_API_KEY_ID, secret_key=APCA_API_SECRET_KEY,
                    base_url=APCA_API_BASE_URL)  # For real trading, don't enter a base_url
# broker base url https://data.alpaca.markets/v2
symb = "TSLA"
pos_held = False

while True:
    print("")
    print("Checking Price")
    # print(api.get_account())
    # print(api.get_asset(symb))
    # api.submit_order(
    #     symbol=symb,
    #     qty=1,
    #     side='buy',
    #     type='market',
    #     time_in_force='day'
    # )
    # api.submit_order(
    #     symbol=symb,
    #     qty=15,
    #     side='buy',
    #     type='market',
    #     time_in_force='day'
    # )
    # market_data = api.get_barset(symb, 'minute', limit=240)  # Get one bar object for each of the past 5 minutes
    market_data = api.get_barset(symb, 'minute', 5)
    print(market_data.df)

    close_list = []  # This array will store all the closing prices from the last 5 minutes
    for bar in market_data[symb]:
        close_list.append(bar.c)  # bar.c is the closing price of that bar's time interval

    close_list = np.array(close_list, dtype=np.float64)  # Convert to numpy array
    ma = np.mean(close_list)
    last_price = close_list[4]  # Most recent closing price

    for price in close_list:
        print(RSI.compute_rsi(price, price))

    print("Moving Average: " + str(ma))
    print("Last Price: " + str(last_price))

    if ma + 0.1 < last_price and not pos_held:  # If MA is more than 10cents under price, and we haven't already bought
        print("Buy")
        api.submit_order(
            symbol=symb,
            qty=30,
            side='buy',
            type='market',
            time_in_force='day'
        )
        pos_held = True
    elif ma - 0.1 > last_price and pos_held:  # If MA is more than 10cents above price, and we already bought
        print("Sell")
        api.submit_order(
            symbol=symb,
            qty=50,
            side='sell',
            type='market',
            time_in_force='day'
        )
        pos_held = False
    time.sleep(60)
