from json import JSONDecodeError

from stock_pandas.math.ma import calc_smma
import requests
from src.getTickers import getAllTickers
from src.importData import *

selected_tickers=[]
tickers = getAllTickers()
#tickers = ["ACAHW"]
for ticker in tickers:
    print('Checking ticker: %s' % ticker)
    url = 'http://www.usjkn.com/usstock/stockDayData'
    myobj = {'code': ticker, 'date': '2021-07-13'}

    x = requests.post(url, data = myobj).content.decode()
    try:
      startIndex = x.find('status')
      res = json.loads(x[startIndex-2:])
      hdly_lastFive = res["hdlyData"][-5:]
    except JSONDecodeError:
      continue

    for i in hdly_lastFive:
        if i >= 150:
            selected_tickers.append(ticker)
            print(selected_tickers)
            break



