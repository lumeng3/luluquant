import sys
import matplotlib.pyplot as plt
from src.getTickers import *
from src.importData import *

def getAvgLastNDaysVolume(self):
    sumVolume = 0
    for i in range(-PLATFORM_DAYS, -1):
        sumVolume += self.dataVolume[i]
    return sumVolume/PLATFORM_DAYS

def getLastNDaysHigh(self):
    lastTenHigh = 0
    for i in range(-PLATFORM_DAYS, -1):
        lastTenHigh = max(self.dataHigh[i], lastTenHigh)
    return lastTenHigh

def getLastNDaysLow(self):
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
        lastNHigh = getLastNDaysHigh(self)
        lastNLow = getLastNDaysLow(self)
        lastNAvgVolume = getAvgLastNDaysVolume(self)
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
        #print('date %s, current price %.2f, previous price %.2f' % (self.datas[0].datetime.datetime(), self.sampleData.close[0], self.sampleData.close[-1]))
        tunShiXian(self, isMoreThanTenDays)
        cutMyLoss(self)
        gainMyProfit(self)


tickers = getTestTickersFromFolder()
#tickers = getAllTickers()

for ticker in tickers:
    #data0 = getDataFromYahooFinance(ticker)
    data0 = getDataFromLocalYahooFinance(ticker)
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
#在止盈止损数据指定后，优化画图部分
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