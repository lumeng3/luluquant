import alpaca_trade_api as alpaca
from datetime import datetime
from local_settings import alpaca_paper
import matplotlib.pyplot as plt


ALPACA_API_KEY = alpaca_paper['api_key']
ALPACA_SECRET_KEY = alpaca_paper['api_secret']
END_POINT = alpaca_paper['url']
ALPACA_PAPER = True

api = alpaca.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, END_POINT)

active_assets = api.list_assets(status='active')

gain_list = []
loss_list = []

for i in range(len(active_assets)):
    exchange = active_assets[i].exchange
    if exchange != 'NASDAQ' :
        continue

    stock_symbol = active_assets[i].symbol
    print(f'examining "{stock_symbol}"')
    barset = api.get_barset(stock_symbol, 'day', limit = 100)
    stock_barset = barset[stock_symbol]
    for j in range(1,len(stock_barset)-10):
        open_t       = stock_barset[j].o
        high_tm1     = stock_barset[j - 1].h
        close_t      = stock_barset[j].c
        low_t        = stock_barset[j].l
        volume_tm1   = stock_barset[j - 1].v
        volume_t     = stock_barset[j].v

        # condition 1: today's open is higher than 1.02 * yesterday's high
        # condition 2: today's volume is higher than 1.2 * yesterday's volume
        # condition 3: today's low is higher than yesterday's high * 1.02 (overwrite condition 1)
        if low_t > high_tm1 * 1.02 and volume_t > volume_tm1 * 1.2 :
            # we found a case
            maximum_gain_percentage = 100.0 * (max([getattr(obj, 'h') for obj in stock_barset[j+1:j+10]]) - close_t) / close_t
            maximum_loss_percentage = 100.0 * (min([getattr(obj, 'l') for obj in stock_barset[j+1:j+10]]) - close_t) / close_t
            gain_list.append(maximum_gain_percentage)
            loss_list.append(maximum_loss_percentage)

plot1 = plt.figure(1)
plt.hist(gain_list)
plot2 = plt.figure(2)
plt.hist(loss_list)
