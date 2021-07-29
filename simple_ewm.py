import pandas as pd 
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr

yf.pdr_override()

stock = input("Enter a ticker symbol: ")
print(stock)

startyear= int(input("From Year? : "))
startmonth= 1
startday= 1

start = dt.datetime(startyear, startmonth, startday)
now = dt.datetime.now()

df = pdr.get_data_yahoo(stock,start,now)
df = df.sort_values('Date')

close = df['Adj Close']
close = pd.DateFrame(data= close)

short = close.ewm(span = 10, adjust = False).mean()
medium = close.ewm(span = 20, adjust = False).mean()
long = close.ewm(span = 40, adjust = False).mean()

close['short'] = short
close['medium'] = medium
close['long'] = long


def buy_sell(data):

    buy_list = []6
    sell_list = []
    flag_long = False
    flag_short = False

    for i in range(0, len(data)):
        if data['medium'][i] < data['long'][i] and data['short'][i] < data['medium'][i] and flag_long == False and flag_short == False:
            buy_list.append(data['Adj Close'][i])
            sell_list.append(np.nan)
            flag_short = True
        elif flag_short == True and data['short'][i] > data['medium'][i]:
            sell_list.append(data['Adj Close'][i])
            buy_list.append(np.nan)
            flag_short = False
        elif data['medium'][i] > data['long'][i] and data['short'][i] > data['medium'][i] and flag_long == False and flag_short == False:
            buy_list.append(data['Adj Close'][i])
            sell_list.append(np.nan)
            flag_long = True
        elif flag_long == True and data['short'][i] < data['medium'][i]:
            sell_list.append(data['Adj Close'][i])
            buy_list.append(np.nan)
            flag_long = False
        else:
            buy_list.append(np.nan)
            sell_list.append(np.nan)

    return (buy_list, sell_list)


close['buy'] = buy_sell(close)[0]
close['sell'] = buy_sell(close)[1]
