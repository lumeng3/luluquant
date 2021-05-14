import json
from get_all_tickers import get_tickers as gt
from get_all_tickers.get_tickers import Region
import sys
import alpaca_backtrader_api
import backtrader as bt
from datetime import datetime
import matplotlib.pyplot as plt

SELECTED_TICKERS = []
SELECTED_END_VALUE = []
SELECTED_FLAG = False
CURRENT_TICKER = ''
CURRENT_SIZE = 0
PREV_VALUE = 0
HOLDING_FLAG = False
ABS_PATH = "/Users/menglu/Downloads/1000day_US"
ALPACA_API_KEY = 'PKGYNPQTC8OD4FF2GS44'
ALPACA_SECRET_KEY = '0s2vro0wYJrbbj0QOfcQ9xYFEHUiMEbpzdwi9rpg'
ALPACA_PAPER = True
PLATFORM_DAYS = 20
PLATFORM_RANGE = 1.05
PLATFORM_CROSSOVER_RANGE = 1.1
HUGE_VOLUME_RANGE = 2
LOSS_RATE = 0.95
GAIN_RATE = 1.2

def getAvgLastTenVolume(self):
    sumVolume = 0
    for i in range(-PLATFORM_DAYS, -1):
        sumVolume += self.dataVolume[i]
    return sumVolume/PLATFORM_DAYS

def getLastTenHigh(self):
    lastTenHigh = 0
    for i in range(-PLATFORM_DAYS, -1):
        lastTenHigh = max(self.dataHigh[i], lastTenHigh)
    return lastTenHigh

def getLastTenLow(self):
    lastTenLow = sys.maxsize
    for i in range(-PLATFORM_DAYS, -1):
        lastTenLow = min(self.dataLow[i], lastTenLow)
    return lastTenLow

def tunShiXian(self, isMoreThanTenDays):
    isLastTenDaysPlatform = False
    isCurrentDayCrossOverPlatform = False
    isCurrentVolumeHuge = False
    isTodayOpenLow = False
    isStockVolumeMoreThan3000 = False

    if isMoreThanTenDays:
        lastNHigh = getLastTenHigh(self)
        lastNLow = getLastTenLow(self)
        lastNAvgVolume = getAvgLastTenVolume(self)
        isTodayOpenLow = self.dataOpen[0] < self.dataClose[-1]
        isLastTenDaysPlatform = (lastNHigh - lastNLow) / lastNLow < PLATFORM_RANGE
        isCurrentDayCrossOverPlatform = self.dataClose[0] > lastNHigh * PLATFORM_CROSSOVER_RANGE
        isCurrentVolumeHuge = self.dataVolume[0] >= lastNAvgVolume * HUGE_VOLUME_RANGE
        isStockVolumeMoreThan3000 = self.dataVolume[0] >= 10000000
        global HOLDING_FLAG
        global SELECTED_FLAG

    if (not HOLDING_FLAG) & isTodayOpenLow & isLastTenDaysPlatform & isCurrentDayCrossOverPlatform & isCurrentVolumeHuge & isStockVolumeMoreThan3000:
        if CURRENT_TICKER not in SELECTED_TICKERS:
            SELECTED_TICKERS.append(CURRENT_TICKER)
        global PREV_VALUE
        PREV_VALUE = cerebro.broker.getvalue()
        purchaseSize = int(PREV_VALUE / self.data.close[0])
        self.buy(size=purchaseSize)
        HOLDING_FLAG = True
        SELECTED_FLAG = True
        global CURRENT_SIZE
        CURRENT_SIZE = CURRENT_SIZE + purchaseSize
        print('Purchased on date %s at price %.2f, for shares %.2f' % (self.datas[0].datetime.datetime(), self.data.close[0], purchaseSize))

def cutMyLoss(self):
    currentValue = cerebro.broker.getvalue()
    global PREV_VALUE
    global HOLDING_FLAG
    if HOLDING_FLAG & (currentValue/PREV_VALUE < LOSS_RATE):
        global CURRENT_SIZE
        print('Cut loss on date %s at price %.2f, for shares %.2f' % (
        self.datas[0].datetime.datetime(), self.data.close[0], CURRENT_SIZE))
        self.sell(size=CURRENT_SIZE)
        HOLDING_FLAG = False
        CURRENT_SIZE = 0
        PREV_VALUE = currentValue

def gainMyProfit(self):
    currentValue = cerebro.broker.getvalue()
    global PREV_VALUE
    global HOLDING_FLAG
    if HOLDING_FLAG & (currentValue / PREV_VALUE >= GAIN_RATE):
        global CURRENT_SIZE
        print('Gain profit on date %s at price %.2f, for shares %.2f' % (
            self.datas[0].datetime.datetime(), self.data.close[0], CURRENT_SIZE))
        self.sell(size=CURRENT_SIZE)
        HOLDING_FLAG = False
        CURRENT_SIZE = 0
        PREV_VALUE = currentValue

class TunShiXian(bt.Strategy):

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataOpen = self.datas[0].open
        self.dataClose = self.datas[0].close
        self.dataHigh = self.datas[0].high
        self.dataLow = self.datas[0].low
        self.dataVolume = self.datas[0].volume
        self.idx = 0

    def next(self):
        isMoreThanTenDays = len(self) > PLATFORM_DAYS
        #print('date %s, current price %.2f, previous price %.2f' % (self.datas[0].datetime.datetime(), self.data.close[0], self.data.close[-1]))
        tunShiXian(self, isMoreThanTenDays)
        cutMyLoss(self)
        gainMyProfit(self)

# with open(ABS_PATH + '/AAPL.json') as file:
#   data = json.load(file)
# store = alpaca_backtrader_api.AlpacaStore(
#     key_id=ALPACA_API_KEY,
#     secret_key=ALPACA_SECRET_KEY,
#     paper=ALPACA_PAPER
# )
# DataFactory = store.getdata
# data0 = DataFactory(dataname='AAPL', historical=True, fromdate=datetime(
#      2021, 3, 1), timeframe=bt.TimeFrame.Days)

tickers = gt.get_tickers(NYSE=False, NASDAQ=True, AMEX=False)
test_tickers = tickers[:300]
bad_tickers = ["AACQW", "AACG","ACAHW","ACEVW","ACKIW"]

for ticker in test_tickers:
    if ticker in bad_tickers:
        continue
    data0 = bt.feeds.YahooFinanceData(
            dataname=ticker,
            name=ticker,
            fromdate=datetime(2018, 5, 13),
            todate=datetime(2021, 5, 13),
            reverse=False
    )

    cerebro = bt.Cerebro()
    cerebro.addstrategy(TunShiXian)
    cerebro.adddata(data0)
    print('----------------------------')
    print('Ticker selected: %s' % ticker)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    CURRENT_TICKER = ticker
    PREV_VALUE = cerebro.broker.getvalue()
    CURRENT_SIZE = 0
    HOLDING_FLAG = False
    SELECTED_FLAG = False
    try:
        cerebro.run()
    except OSError:
        continue
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    if SELECTED_FLAG:
        SELECTED_END_VALUE.append(cerebro.broker.getvalue()/10000 - 1)
    # cerebro.plot()

print(SELECTED_TICKERS)
print(SELECTED_END_VALUE)

plt.style.use('ggplot')
x_pos = [i for i, _ in enumerate(SELECTED_TICKERS)]

plt.bar(x_pos, SELECTED_END_VALUE, color='green')
plt.xlabel("tickers")
plt.ylabel("%")
plt.title("BackTrade Result")
plt.xticks(x_pos, SELECTED_TICKERS)
plt.show()