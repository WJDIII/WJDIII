#!/usr/bin/env python
# coding: utf-8

# In[1]:


import quandl
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import requests
import statsmodels.api as sm
import statsmodels.tsa.stattools as ts
from statsmodels.tsa.vector_ar.vecm import coint_johansen
from sklearn import linear_model
from math import floor


# In[2]:


eth = pd.read_csv("ETHUSDT.csv")
ltc = pd.read_csv("LTCUSDT.csv")

eth = np.log(eth['close'])
ltc = np.log(ltc['close'])

eth_ltc_pairs = pd.concat([eth, ltc], axis = 1).dropna()
eth_ltc_pairs.columns = ['eth_close', 'ltc_close']
eth_ltc_pairs.head()


# In[3]:


eth_ltc_pairs['Price Ratio eth/ltc'] = eth_ltc_pairs['eth_close'] / eth_ltc_pairs['ltc_close']
eth_ltc_pairs['Log Spread rth/ltc'] = eth_ltc_pairs['eth_close'] - eth_ltc_pairs['ltc_close']
log_prices = eth_ltc_pairs
log_prices.head()


# In[4]:


assets = ['ethUSDT', 'ltcUSDT', 'Price Ratio', 'Log Spread']
plt.figure(figsize = (15, 10))
plt.plot(log_prices)
plt.xlabel('days')
plt.title('Performance of cryptocurrencies')
plt.legend(assets)
plt.show()


# In[5]:


def reg(x,y):
    regr = linear_model.LinearRegression()
    x_constant = pd.concat([x,pd.Series([1]*len(x), index = x.index)], axis=1)
    regr.fit(x_constant, y)
    beta = regr.coef_[0]
    alpha = regr.intercept_
    spread = y - x*beta - alpha
    return spread


# In[6]:


x = log_prices['eth_close']
y = log_prices['ltc_close']
spread = reg(x,y)
#plotting the spread of the series
spread.plot(figsize=(15,10))
plt.ylabel('spread')


# In[7]:


adf = sm.tsa.stattools.adfuller(spread, maxlag=1)
print ('ADF test Statistic: %.02f' % adf[0])
for key, value in adf[4].items():
    print('\t%s: %.3f' % (key, value))
print ('p-value: %.03f' % adf[1])


# In[8]:


print(adf)


# In[11]:


spread.head()


# In[24]:


mu = spread.mean()
sigma = spread.std()
x = spread
bins = 25

print(mu)
print(sigma)


# In[25]:


plt.hist(spread, bins, facecolor='blue', alpha=0.5)


# In[26]:


def zscore(series):
    return (series - series.mean() / np.std(series))

eth.head()


# In[27]:


#dataframe that contains trading signals
signals = pd.DataFrame()
signals['asset1'] = eth
signals['asset2'] = ltc
ratios = eth/ltc


# In[28]:


#z score and upper/lower trading thresholds


# In[ ]:




