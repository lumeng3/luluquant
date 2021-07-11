from datetime import timedelta

import numpy as np
from stock_pandas import StockDataFrame
import yfinance as yf

from src.getTickers import getAllTickers
from src.importData import *

hdly_DAYS = 2000
selected_tickers=[]
tickers = getAllTickers()

#tickers = ["BTX"]
for ticker in tickers:
    print('Checking ticker: %s' % ticker)
    currDate = datetime.today() - timedelta(days=hdly_DAYS)
    tickerInfo = yf.Ticker(ticker)
    df = tickerInfo.history(period="1000d")
    df = df.rename(columns={"Open": "open", "Close": "close", "High": "high", "Low": "low", "Volumn":"volumn"})
    stock = StockDataFrame(
        df
    )

    N = 3
    stock["DateTime"] = stock.index
    stock["hhv485"] = stock['hhv:485,high']
    stock["var1"] = stock['ma:17,hhv485']

    stock["hhv222"] = stock['hhv:222,high']
    stock["var2"] = stock['ma:17,hhv222']

    stock["hhv96"] = stock['hhv:96,high']
    stock["var3"] = stock['ma:17,hhv96']

    stock["llv485"] = stock['llv:485,low']
    stock["var4"] = stock['ma:17,llv485']

    stock["llv222"] = stock['llv:222,low']
    stock["var5"] = stock['ma:17,llv222']

    stock["llv96"] = stock['llv:96,low']
    stock["var6"] = stock['ma:17,llv96']

    stock["var7_1"] = (stock["var4"]*0.96 + stock["var5"]*0.96 + stock["var6"]*0.96 + stock["var1"]*0.558 + stock["var2"]*0.558 + stock["var3"]*0.558)/6
    stock["var7"] = stock['ma:17,var7_1']

    stock["var8_1"] = (stock["var4"]*1.25 + stock["var5"]*1.23 + stock["var6"]*1.2 + stock["var1"]*0.55 + stock["var2"]*0.55 + stock["var3"]*0.65)/6
    stock["var8"] = stock['ma:17,var8_1']

    stock["var9_1"] = (stock["var4"]*1.3 + stock["var5"]*1.3 + stock["var6"]*1.3 + stock["var1"]*0.68 + stock["var2"]*0.68 + stock["var3"]*0.68)/6
    stock["var9"] = stock['ma:17,var9_1']

    stock["varA_1"] = (stock["var7"] * 3 + stock["var8"] * 2 + stock["var9"])/6 * 1.738
    stock["varA"] =stock['ma:17,varA_1']

    stock["Date"] = stock.index
    stock["Date"] = np.where(stock["Date"].dt.day == 1, 30, stock["Date"].dt.day - 1)
    stock["varB"] = stock["varA"] * stock["Date"]
    #stock["varC"] = stock["low"]
    stock["varD"] = stock['low'].shift(1)
    stock["varE_1"] = abs(stock['low']-stock["varD"]) #ABS(VARC - VARD)
    stock["varE_2"] = stock['ema:3,varE_1']
    stock['varE_3'] = np.where(stock['low']-stock["varD"] > 0, stock['low']-stock["varD"], 0) #MAX(VARC - VARD, 0)
    stock["varE_4"] = stock['ema:3,varE_3']
    stock["varE"] = stock["varE_2"] / stock["varE_4"] * 100

    stock['varF_1'] = np.where(stock['close'] * 1.35 <= stock["varB"], stock["varE"] * 10, stock["varE"] / 10)  # MAX(VARC - VARD, 0)
    stock["varF"] = stock['ma:3,varF_1']

    stock["var10"] = stock['llv:30,low']
    stock["var11"] = stock['hhv:30,varF']

    VAR12 = 100

    stock["final_1"] = (stock["varF"] + stock["var11"] * 2) / 2
    stock["final_2"] = np.where(stock['low'] <= stock["var10"], stock["final_1"], 0)  # MAX(VARC - VARD, 0)
    stock["final"] = stock['ma:3,final_2']

    for i in stock["final"].iloc[-7:-1]:
        if i > 0:
            selected_tickers.append(ticker)

print(selected_tickers)



