import json
import alpaca_backtrader_api
import requests
import quandl
import pandas

from src.constants import *
import backtrader as bt
from datetime import datetime

def getDataFromJson(ticker):
    with open(ABS_PATH + '/' + ticker +'.json') as file:
      data0 = json.load(file)
    return data0

def getDataFromAlpaca(ticker):
    store = alpaca_backtrader_api.AlpacaStore(
        key_id=ALPACA_API_KEY,
        secret_key=ALPACA_SECRET_KEY,
        paper=ALPACA_PAPER
    )
    DataFactory = store.getdata
    data0 = DataFactory(dataname=ticker, historical=True, fromdate=datetime(
        2018, 3, 1), timeframe=bt.TimeFrame.Days)
    return data0

def getDataFromQuandl(ticker):
    quandl.ApiConfig.api_key = QUANDL_API_KEY
    df = quandl.get_table('ZACKS/FC',ticker=ticker, paginate=True)
    df.rename(columns={'settle': 'close', 'prev_day_open_interest': 'openinterest'}, inplace=True)
    return df

def getDataFromYahooFinance(ticker):  #Yahoo sucks
    data0 = bt.feeds.YahooFinanceData(
            dataname=ticker,
            name=ticker,
            fromdate=datetime(2020, 12, 5),
            todate=datetime(2021, 6, 14),
            reverse=False
    )
    return data0

def getDataFromLocalYahooFinance(ticker):
    fileName = SAMPLE_PATH + '/' + ticker + '.csv'
    data0 = bt.feeds.YahooFinanceCSVData(
            dataname=fileName,
            name=ticker,
            fromdate=datetime(2021, 3, 11),
            todate=datetime(2021, 6, 11)
    )
    return data0