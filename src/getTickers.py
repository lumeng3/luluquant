from get_all_tickers import get_tickers as gt
import os

from src.constants import SAMPLE_PATH


def getAllTickers():
    tickers = gt.get_tickers(NYSE=False, NASDAQ=True, AMEX=False)
    return tickers

def getTestTickersFromFolder():
    arrs = os.listdir(SAMPLE_PATH)
    tickers = [x[:-4] for x in arrs]
    return tickers
