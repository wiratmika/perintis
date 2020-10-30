from datetime import datetime
from typing import Tuple

import requests
import streamlit

from exceptions import InvalidSessionException


@streamlit.cache
def scrape_stocks():
    data = {}

    url = "https://scanner.tradingview.com/indonesia/scan"
    payload = '{"filter":[{"left":"market_cap_basic","operation":"nempty"},{"left":"type","operation":"in_range","right":["stock","dr","fund"]},{"left":"subtype","operation":"in_range","right":["common","","etf","unit","mutual","money","reit","trust"]}],"options":{"data_restrictions":"PREV_BAR","lang":"id_ID"},"symbols":{"query":{"types":[]},"tickers":[]},"columns":["name","close","description"],"sort":{"sortBy":"market_cap_basic","sortOrder":"desc"},"range":[0,300]}'  ## noqa

    print("Calling price API...")
    response = requests.post(url, payload).json()["data"]
    for content in response:
        info = content["d"]
        symbol = info[0]
        price = info[1]
        name = info[2]
        data[symbol] = (name, price)

    return data


@streamlit.cache
def scrape_stockbit(credentials: Tuple[str, str]):
    headers = {
        "x-pin": credentials[1],
        "authorization": f"Bearer {credentials[0]}",
    }

    today = datetime.now().date().strftime("%Y-%m-%d")
    url = f"https://api.stockbit.com/v2.4/trade/report/trade_activity?start=1970-01-01&end={today}"
    print("Calling Stockbit trade API...")
    trade = requests.get(url, headers=headers).json()["data"]["result"]

    url = "https://api.stockbit.com/v2.4/trade/order?gtc=1"
    print("Calling Stockbit order API...")
    response = requests.get(url, headers=headers).json()

    if response.get("error") == "INVALID_SESSION":
        raise InvalidSessionException
    order = response["data"]

    return {
        "trade": trade,
        "order": order,
    }
