import yfinance as yf
import numpy as np
import pandas as pd
from functools import reduce

# Use load_ticker to load the ticker information sent as parameter and the industry information price
def load_ticker(ticker, industry='SPY', start=START, end=END):
    ticker_data = yf.download(ticker, start=start, end=end)
    
    ticker_data = ticker_data[['Close', 'Volume', 'High', 'Low']].rename(columns={'Close': 'Close_Price_%s' % (ticker), 'Volume': 'Volume', 'High': 'High_Price', 'Low': 'Low_Price'}) 
    industry_data = yf.download(industry, start=START, end=END)[['Close']].rename(columns={'Close': 'Close_Price_%s'% (industry)})
    ticker_data = pd.merge(ticker_data, industry_data, how='left', on='Date')
    return ticker_data

# Nix returns a list without the VALUE sent as parameter
def nix(value, list):
    return [x for x in list if x!=value]

def calculate_sma(days, df, ticker):
  sma_df = df['Close_Price_%s' % (ticker)].rolling(window=days).mean().to_frame()
  return sma_df.rename(columns={'Close_Price_%s' % (ticker):'%s_sma' % (ticker)})

def calculate_rsi(df, ticker):
    delta = df['Close_Price_%s' % (ticker)].diff()
    positive = delta.clip(lower=0)
    negative = -delta.clip(upper=0)
    ema_positive = positive.ewm(alpha=1/14, min_periods=14).mean()
    ema_negative = negative.ewm(alpha=1/14, min_periods=14).mean()
    rsi = 100 - 100 / (1 + ema_positive / ema_negative)
    rsi = rsi.to_frame()
    return rsi.rename(columns={'Close_Price_%s' % (ticker):'%s_rsi' % (ticker)})

def merge_dfs(dfs_list):
  merged_df = reduce(lambda left, right: pd.merge(left, right, on='Date'), dfs_list)
  return merged_df.dropna()