import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

TICKERS = ['AAPL', 'AMZN', 'TSLA', 'IBM']
START_DATE = '2012-01-01'
END_DATE = '2022-01-01'
TRADING_DAYS = 252
NUM_PORTFOLIOS = 10000


def download_data():
    stocks = {}
    for ticker in TICKERS:
        t = yf.Ticker(ticker)
        stocks[ticker] = t.history(start=START_DATE, end=END_DATE)['Close']

    return pd.DataFrame(stocks)


def plot_data(data):
    data.plot(figsize=(10,5 ))
    plt.show()


def calculate_return(data):
    return np.log(data/data.shift(1))


def show_statistics(daily_returns):
    print(daily_returns.mean() * TRADING_DAYS)
    print(daily_returns.cov() * TRADING_DAYS)


def show_mean_variance(returns, weights):
    # we are after the annual return
    portfolio_return = np.sum(returns.mean() * weights) * TRADING_DAYS
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov()
                                                            * TRADING_DAYS, weights)))
    print("Expected portfolio mean (return): ", portfolio_return)
    print("Expected portfolio volatility (standard deviation): ", portfolio_volatility)


def generate_portifolio(returns):
    portfolio_means = []
    portfolio_risks = []
    portifolio_weights = []

    for _ in range(NUM_PORTFOLIOS):
        w = np.random.random(len(stocks))
        w = w/np.sum(w)
        portifolio_weights.append(w)
        portfolio_means.append(np.sum(returns.mean() * w) * TRADING_DAYS)
        portfolio_risks.append(np.sqrt(np.dot(w.T, np.dot(returns.cov()
                                                          * TRADING_DAYS, w))))

    return np.array(portifolio_weights), np.array(portfolio_means), np.array(portfolio_risks)

def show_portfolios(returns, volatilities):
    plt.figure(figsize=(10, 6))
    plt.scatter(volatilities, returns, c=returns / volatilities, marker='o')
    plt.grid(True)
    plt.xlabel('Expected Volatility')
    plt.ylabel('Expected Return')
    plt.colorbar(label='Sharpe Ratio')
    plt.show()


if __name__ == '__main__':
    stocks = download_data()
    plot_data(stocks)
    log_daily = calculate_return(stocks)
    show_statistics(log_daily)
    weights, means, risks = generate_portifolio(log_daily)