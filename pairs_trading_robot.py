import websocket
import json
import pprint 
import config 
import numpy as np
import pandas as pd
#import talib
from binance.client import Client
from binance.enums import *
from sklearn import linear_model
import statsmodels.api as sm

#socket to stream minute by minute data
socket = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m/ltcusdt@kline_1m"
#client configuration
client = Client(config.api_key, config.api_secret, tld='us')
#list to append closed values
eth_close = []
ltc_close = []
#Trading Threshold
Threshold = 1.5
#1st Step: Engle-Granger two-step method
#Step 1 Regress on series on another 
def reg(x,y):
    regr = linear_model.LinearRegression
    x_constant = pd.concat([x, pd.Series([1]*len(x), index = x.index)], axis = 1)
    regr.fit(x_constant, y)
    beta = regr.coef_[0]
    alpha = regr.intercept_
    spread = y - x*beta - alpha
    return spread
#Function to create orders on binance
def order(symbol, quantity, side, order_type=ORDER_TYPE_MARKET):
    try:
        print("Sending Order")
        order = client.create_order(symbol=symbol,
        side = side,
        type = order_type,
        quantity = quantity)
    except Exception as e:
        return False

    return True

def on_open(ws):
    print('Wake Up Neo')

def on_close(ws):
    print('Closed Connection')

def on_message(ws, message):

    print('Received Message')
    json_message = json.loads(message)
    pprint.pprint(json_message)

    candle = json_message['k']
    is_candle_closed = candle['x']
    ticker = json_message['s']
    print(ticker)
    close = candle['c']

    if  ticker == 'ETHUSDT' and is_candle_closed:
        print("candle closed at {}".format(close))
        eth_close.append(float(close))
        print("eth closes")
        print(eth_close)
    if  ticker == 'LTCUSDT' and is_candle_closed:
        print("candle closed at {}".format(close))
        ltc_close.append(float(close))
        print("ltc closes")
        print(ltc_close)

        df1 = pd.DataFrame()
        df1['eth close'] = pd.Series(eth_close)
        df1['ltc close'] = pd.Series(ltc_close)
        df1['log eth'] = np.log(df1['eth close'])
        df1['log ltc'] = np.log(df1['ltc close'])

        if len(eth_close) and len(ltc_close) == 250:
            x = df1['log eth']
            y = df1['log ltc']
            spread = reg(x,y)
            #Step 2 Engel Granger Method
            adf = sm.tsa.stattools.adfuller(spread, maxlag=1)
            print('ADF Test Statistic:%.2f' % adf[0])
            print('p-value: %.3f' % adf[1])
            mean = np.mean(spread)
            std = np.std(spread)
            ratio = df1['eth close'] / df1['ltc close']
            df1['mean spread'] = mean
            df1['std spread'] = std
            df1['ratio'] = ratio

        #if spread[-1] > mean + Threshold * std:
            #buy/sell logic here

        #elif spread[-1] < mean +Threshold * std:
            #inverted buy sell logic here

        #else:
            #liquidate logic here 

#websocket for:
#Ethereum + Litecoin
ws = websocket.WebSocketApp(socket, on_open=on_open,
                            on_close=on_close, on_message=on_message)
ws.run_forever()






