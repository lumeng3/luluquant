
from src.getTickers import *
from src.importData import *
import backtrader.indicators as btind
import datetime
GOINGDOWN_DAYS = 485

def hasNotIncreaseTooMuch(datahigh,datalow):
    heighest=0
    lowest=10000
    for i in range(-5, 0):
        heighest = max(heighest, datahigh[i])
        lowest = min(lowest, datalow[i])
    return datahigh < datalow*1.3


class hdly(bt.Strategy):
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataClose = self.datas[0].close
        self.dataHigh = self.datas[0].high
        self.dataLow = self.datas[0].low
        llv485 = btind.Lowest(self.dataLow, period=485)
        hhv485 = btind.Highest(self.dataHigh, period=485)

    def next(self):
        dayenough = len(self) > GOINGDOWN_DAYS
        today = datetime.today()
        curdate = self.datetime.date(ago=0)  # 0 is the default
        if(dayenough and curdate==today):
            SELECTED_TICKERS.append(CURRENT_TICKER)


tickers = getAllTickers()
for ticker in tickers:
    data0 = getDataFromYahooFinance(ticker)
    cerebro = bt.Cerebro()
    cerebro.addstrategy(hdly)
    cerebro.adddata(data0)
    # print('----------------------------')
    print('Checking ticker: %s' % ticker)
   # print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    CURRENT_TICKER = ticker
    SELECTED_FLAG = False
    try:
        cerebro.run()
    except OSError:
        continue
    except IndexError:
        continue

print(SELECTED_TICKERS)
