import os
import numpy as np
import pandas as pd

DEFAULT_TICKERS = ['GOOG', 'JPM', 'MCD', "HYG"]
START, END = "2010-01-01", "2020-01-01"

ticker = 'JPM'
jpm = load_ticker(ticker)
jpm_rsi = calculate_rsi(jpm, "JPM")
jpm_sma = calculate_sma(20, jpm, "JPM")

jpm_final = merge_dfs([jpm, jpm_rsi, jpm_sma])