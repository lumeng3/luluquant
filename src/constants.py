SELECTED_TICKERS = []
SELECTED_END_VALUE = []
SELECTED_FLAG = False
CURRENT_TICKER = ''
CURRENT_SIZE = 0
PREV_VALUE = 0
HOLDING_FLAG = False
ABS_PATH = "SET UP YOUR PATH OF JSON FILES FOLDER"  #/Users/lulu/Downloads/1000day_US
SAMPLE_PATH = "./sampleData"
PLATFORM_DAYS = 20
PLATFORM_RANGE = 1.05
PLATFORM_CROSSOVER_RANGE = 1.1
HUGE_VOLUME_RANGE = 2
LOSS_RATE = 0.95
GAIN_RATE = 1.2

ALPACA_API_KEY = 'PKGYNPQTC8OD4FF2GS44' #Go to Alpaca to find your own api key
ALPACA_SECRET_KEY = '0s2vro0wYJrbbj0QOfcQ9xYFEHUiMEbpzdwi9rpg'
ALPACA_PAPER = True  #True when test in paper account

QUANDL_API_KEY = "fDoLZUz5a9rcT4LKQMfs"

#wscat -c wss://socket.polygon.io/stocks
#{"action":"auth","params":"PKGYNPQTC8OD4FF2GS44"}

# wscat -c wss://stream.data.alpaca.markets/v2/iex
# {"action": "auth", "key": "PKGYNPQTC8OD4FF2GS44", "secret": "0s2vro0wYJrbbj0QOfcQ9xYFEHUiMEbpzdwi9rpg"}
# {"action":"subscribe","trades":[],"quotes":["AAPL"],"bars":["AAPL"]}