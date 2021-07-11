import math

from src.getTickers import *
from src.importData import *
from backtrader.indicators import ema
import datetime
GOINGDOWN_DAYS = 60

def hasNotIncreaseTooMuch(datahigh,datalow):
    heighest=0
    lowest=10000
    for i in range(-5, 0):
        heighest = max(heighest, datahigh[i])
        lowest = min(lowest, datalow[i])
    return datahigh < datalow*1.3

def todayIsLowest(dataclose):
    lowestClose = 10000
    for i in range(-GOINGDOWN_DAYS, -1):
        lowestClose = min(lowestClose, dataclose[i])
    return dataclose[0] <= lowestClose

def todayIsLowestClose(datalastclose,datalow):
    lowest = 10000
    for i in range(-GOINGDOWN_DAYS, -1):
        lowest = min(lowest, datalow[i])
    return datalastclose <= lowest

def findHighest(dataHighest):
    maxPrice = 0
    for i in range(-len(dataHighest)+1,0):
        maxPrice = max(maxPrice, dataHighest[i])
    return maxPrice

class zhaoMaoPiao(bt.Strategy):
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.ema18 = bt.ind.EMA(self.data, period=18)
        self.ema60 = bt.ind.EMA(self.data, period=60)
        self.dataClose = self.datas[0].close
        self.dataHigh = self.datas[0].high
        self.dataLow = self.datas[0].low

    def next(self):
        isGoingDownLongEnough = len(self) > GOINGDOWN_DAYS
        today = datetime.date(2021, 6, 11)
        curdate = self.datetime.date(ago=0)  # 0 is the default
        if(isGoingDownLongEnough and curdate==today):
            compareData = findHighest(self.dataHigh)
            print(curdate)
            if(self.dataClose[0] < compareData/1.5 and
               todayIsLowest(self.dataClose) and
              self.dataClose[0] < 20):
               if CURRENT_TICKER not in SELECTED_TICKERS:
                   print(CURRENT_TICKER)
                   print(curdate)
                   print(self.dataClose[0])
                   print(compareData)
                   SELECTED_TICKERS.append(CURRENT_TICKER)


        #print('date %s, current price %.2f, previous price %.2f' % (self.datas[0].datetime.datetime(), self.sampleData.close[0], self.sampleData.close[-1]))



tickers = getAllTickers()
for ticker in tickers:
    data0 = getDataFromYahooFinance(ticker)
    cerebro = bt.Cerebro()
    cerebro.addstrategy(zhaoMaoPiao)
    cerebro.adddata(data0)
    # print('----------------------------')
    print('Checking ticker: %s' % ticker)
   # print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    CURRENT_TICKER = ticker
    SELECTED_FLAG = False

    cerebro.run()


print(SELECTED_TICKERS)
