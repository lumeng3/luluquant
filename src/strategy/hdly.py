from datetime import timedelta
from json import JSONDecodeError

import numpy as np
from stock_pandas import StockDataFrame
import yfinance as yf
from stock_pandas.math.ma import calc_smma

from src.getTickers import getAllTickers
from src.importData import *

def getRegularHDLY(ticker):
    hdly_DAYS = 2000
    selected_tickers = []
    # tickers = getAllTickers()

    # 执行前，打开stock_panda里面的time_frame文件夹下面 有一个common.py
    # 需要把62行 替换成下面代码
    # column_enums = partial(create_enum, [
    #     'open',
    #     'high',
    #     'low',
    #     'close',
    #     "hhv485","hhv222","hhv96","llv485","llv222","llv96",
    #     "var7_1","var8_1","var9_1","varA_1","varE_1","varE_3",
    #     "varF_1","varF","final_2"
    # ], 'column')
    print('Checking ticker: %s' % ticker)
    currDate = datetime.today() - timedelta(days=hdly_DAYS)
    tickerInfo = yf.Ticker(ticker)
    try:
        df = tickerInfo.history(period="5000d", interval="1d")  # 1wk 1d
    except JSONDecodeError:
        return

    df = df.rename(columns={"Open": "open", "Close": "close", "High": "high", "Low": "low", "Volumn": "volumn"})
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

    stock["var7_1"] = (stock["var4"] * 0.96 + stock["var5"] * 0.96 + stock["var6"] * 0.96 + stock["var1"] * 0.558 +
                       stock["var2"] * 0.558 + stock["var3"] * 0.558) / 6
    stock["var7"] = stock['ma:17,var7_1']

    stock["var8_1"] = (stock["var4"] * 1.25 + stock["var5"] * 1.23 + stock["var6"] * 1.2 + stock["var1"] * 0.55 +
                       stock["var2"] * 0.55 + stock["var3"] * 0.65) / 6
    stock["var8"] = stock['ma:17,var8_1']

    stock["var9_1"] = (stock["var4"] * 1.3 + stock["var5"] * 1.3 + stock["var6"] * 1.3 + stock["var1"] * 0.68 +
                       stock["var2"] * 0.68 + stock["var3"] * 0.68) / 6
    stock["var9"] = stock['ma:17,var9_1']

    stock["varA_1"] = (stock["var7"] * 3 + stock["var8"] * 2 + stock["var9"]) / 6 * 1.738
    stock["varA"] = stock['ma:17,varA_1']

    stock["Date"] = stock.index
    try:
        stock["Date"] = np.where(stock["Date"].dt.day == 1, 30, stock["Date"].dt.day - 1)
    except AttributeError:
        return
    stock["varB"] = stock["varA"] * stock["Date"]
    # stock["varC"] = stock["low"]
    stock["varD"] = stock['low'].shift(1)
    stock["varE_1"] = abs(stock['low'] - stock["varD"])  # ABS(VARC - VARD)
    stock["varE_2"] = calc_smma(stock['varE_1'].to_numpy(), 3)  # stock['smma:3,varE_1']
    stock['varE_3'] = np.where(stock['low'] - stock["varD"] > 0, stock['low'] - stock["varD"],
                               0)  # MAX(VARC - VARD, 0)
    stock["varE_4"] = calc_smma(stock['varE_3'].to_numpy(), 3)  # stock['smma:3,varE_3']
    stock["varE"] = stock["varE_2"] / stock["varE_4"] * 100

    stock['varF_1'] = np.where(stock['close'] * 1.35 <= stock["varB"], stock["varE"] / 10,
                               stock["varE"] * 10)  # MAX(VARC - VARD, 0)
    stock["varF"] = stock['ma:3,varF_1']

    stock["var10"] = stock['llv:30,low']
    stock["var11"] = stock['hhv:30,varF']

    VAR12 = 1990831

    stock["final_1"] = (stock["varF"] + stock["var11"] * 2) / 2
    stock["final_2"] = np.where(stock['low'] <= stock["var10"], stock["final_1"], 0)  # MAX(VARC - VARD, 0)
    stock["final"] = stock['ma:3,final_2']

    return df


# stock.to_excel("/Users/menglu/Desktop/"+ticker+"_output.xlsx")
#
# for i in stock["final"].iloc[-7:-1]:
#     if i > 0:
#         print("found ticker" + ticker)
#         selected_tickers.append(ticker)
#         print(selected_tickers)
#         break

# if(stock["final"][-1] > 20000 and stock["final"][-2] == 0):
#      print("found ticker" + ticker)
#      selected_tickers.append(ticker)
#      print(selected_tickers)

# print(selected_tickers)




# tickers = ["AAPL", "SOFI", "NFLX", "SAM", "ABNB"]
# for ticker in tickers:
#     getRegularHDLY(ticker)
