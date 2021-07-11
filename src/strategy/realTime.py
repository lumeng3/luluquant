import websocket, json
import requests
from datetime import datetime, timedelta, time

from pytz import timezone

#代码没有写完，回踩GMMA的功能被trading view能更好的实现，这个代码写到了计算EMA六条线，只要补齐realtime数据回踩的部分就可以使用了。

ALPACA_API_KEY = 'PKGYNPQTC8OD4FF2GS44' #Go to Alpaca to find your own api key
ALPACA_SECRET_KEY = '0s2vro0wYJrbbj0QOfcQ9xYFEHUiMEbpzdwi9rpg'


# EMA=Price(t)×k+EMA(y)×(1−k)
# where:
# t=today
# y=yesterday
# N=number of days in EMA
# k=2÷(N+1)


def ema(values, period):
    return ta.ema(values, length=period)

def on_open(ws):
    auth_data = {
        "action": "auth",
        "key": ALPACA_API_KEY,
        "secret": ALPACA_SECRET_KEY
    }
    chanel_data = {
        "action": "subscribe",
        "trades": [],
        "quotes": ["AAPL"],
        "bars": ["AAPL"]
    }
    ws.send(json.dumps(auth_data))
    ws.send(json.dumps(chanel_data))

def on_message(ws, message):
    m = json.loads(message)
    currentPrice = (m[0]['ap'] + m[0]['bp'])/2
    print(currentPrice)

def on_close(ws):
    print("closed")

timeFrame = "30Min"
header = {
   "APCA-API-KEY-ID":ALPACA_API_KEY,
   "APCA-API-SECRET-KEY":ALPACA_SECRET_KEY
}
closePrice = []

for t in range(0, 10):
    bar_base_url = "https://data.alpaca.markets/v2/stocks/aapl/bars?start={startTime}&end={endTime}&timeframe={timeFrame}"

    currDate = datetime.today() - timedelta(days=t)
    startTime = currDate.strftime('%Y-%m-%d') + "T13:30:00Z"
    endTime = currDate.strftime('%Y-%m-%d') + "T19:30:00Z"
    #using Chicago Time since I'm in Chicago
    marketOpenTime = time(8, 00)
    marketCloseTime = time(14, 30)

    if t == 0:
        bar_base_url = bar_base_url.replace("{startTime}", startTime).replace("&end={endTime}", "").replace("{timeFrame}", timeFrame)
    else:
        bar_base_url=bar_base_url.replace("{startTime}", startTime).replace("{endTime}", endTime).replace("{timeFrame}", timeFrame)

    r = requests.get(bar_base_url, headers=header)
    r_request = json.loads(json.dumps(r.json()))

    for i in reversed(r_request["bars"]):
        i['t'] = datetime.fromisoformat(i['t'].replace('Z', '-00:00')).astimezone(timezone('US/Central'))
        if(marketOpenTime <= i['t'].time() <= marketCloseTime):
            closePrice.append(i['c'])

gmma_days = [30, 35, 40, 45, 50, 60]
gmma_values = []
for d in gmma_days:
    tempPriceList = closePrice[0:d]
    currEMA = ema(reversed(tempPriceList), d)
    gmma_values.append(currEMA)

print(closePrice)
print(gmma_values)

# socket = "wss://stream.data.alpaca.markets/v2/iex"
# ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)
# ws.run_forever()
