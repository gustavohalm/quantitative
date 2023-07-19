import datetime

import numpy as np
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm


def download_data(stock, start_date, end_date):
    # name of the stock (key) - stock values (2010-1017) as the values
    stock_data = {}

    stock_data[stock] = yf.download(stock, start_date, end_date)['Adj Close']

    return pd.DataFrame(stock_data)


# calculate the value at risk for tomorrow
def calculate_vars(position, c, mu, sigma):
    v = norm.ppf(1 - c)
    var = position * (mu - sigma * v)

    return var


def calculate_vars_multi(position, c, mu, sigma, n ):
    v = norm.ppf(1 - c)
    var = position * (mu * n - sigma * np.sqrt(n) * v)

    return var

if __name__:
    start = datetime.datetime(2014, 1, 1)
    end = datetime.datetime(2018, 1, 1)

    ticker_appl = download_data('AAPL', start, end)
    ticker_tsla = download_data('TSLA', start, end)
    ticker_cpfl = download_data('CPFE3.SA', start, end)

    ticker_appl['returns'] = np.log(ticker_appl['AAPL'] / ticker_appl['AAPL'].shift(1))
    print(ticker_appl)
    ticker_appl = ticker_appl[1:]
    investment = 1000000
    c = 0.95
    mu = np.mean(ticker_appl['returns'])
    sigma = np.std(ticker_appl['returns'])

    vars = calculate_vars(investment, c, mu, sigma)

    print('Value At Risk', vars)
    print('Value At Risk 7 days', calculate_vars_multi(investment, c, mu, sigma, 7))
