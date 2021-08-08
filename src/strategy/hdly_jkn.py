from json import JSONDecodeError

from stock_pandas.math.ma import calc_smma
import requests
from src.getTickers import getAllTickers
from src.importData import *
import pandas as pd


def gethdlyjkn(ticker):
    selected_tickers = []
    # tickers = getAllTickers()
    print('Checking ticker: %s' % ticker)
    url = 'http://www.usjkn.com/usstock/stockDayData'
    myobj = {'code': ticker, 'date': '2021-08-02'}

    x = requests.post(url, data=myobj).content.decode()
    try:
        startIndex = x.find('status')
        res = json.loads(x[startIndex - 2:])
        df = pd.DataFrame(data=res["hdlyData"])
        return df
        # hdly_lastFive = res["hdlyData"]
        # df.to_excel("/Users/menglu/Desktop/" + ticker + "_jkn_output.xlsx")
    except JSONDecodeError:
        return

    # for i in hdly_lastFive:
    #     if i >= 150:
    #         selected_tickers.append(ticker)
    #         print(selected_tickers)
    #         break
    #



# tickers = ["AAPL", "SOFI", "NFLX", "SAM", "ABNB"]
# gethdlyjkn(tickers)