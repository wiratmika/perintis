from datetime import datetime
from typing import Tuple

import requests
import streamlit

from exceptions import InvalidSessionException


@streamlit.cache
def scrape_stocks():
    data = {}

    url = "https://scanner.tradingview.com/indonesia/scan"
    payload = '{"filter":[{"left":"market_cap_basic","operation":"nempty"},{"left":"type","operation":"in_range","right":["stock","dr","fund"]},{"left":"subtype","operation":"in_range","right":["common","","etf","unit","mutual","money","reit","trust"]}],"options":{"data_restrictions":"PREV_BAR","lang":"id_ID"},"symbols":{"query":{"types":[]},"tickers":[]},"columns":["name","close","description","market_cap_basic"],"sort":{"sortBy":"market_cap_basic","sortOrder":"desc"},"range":[0,300]}'  ## noqa

    print("Calling price API...")
    response = requests.post(url, payload).json()["data"]
    for content in response:
        info = content["d"]
        symbol = info[0]
        price = info[1]
        name = info[2]
        market_cap = info[3]
        data[symbol] = (name, price, market_cap)

    return data


@streamlit.cache
def scrape_stockbit(token):
    headers = {
        "authorization": f"Bearer {token}",
    }

    url = f"https://trading.masonline.id/portfolio"
    print("Calling Stockbit portfolio API...")
    portfolio = requests.get(url, headers=headers).json()["data"]["result"]

    return {
        "portfolio": portfolio,
    }


@streamlit.cache
def get_indices():
    url = "https://raw.githubusercontent.com/wiratmika/indonesia-stock-indices/main/idx30.json"
    return {"IDX30": requests.get(url).json()}
