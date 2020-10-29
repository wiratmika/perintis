from datetime import datetime

import requests
import streamlit

from data import dates, issuers, write


@streamlit.cache
def scrape():
    data = {}
    for code in issuers.keys():
        data[code] = None

    url = "https://scanner.tradingview.com/indonesia/scan"
    payload = '{"filter":[{"left":"market_cap_basic","operation":"nempty"},{"left":"type","operation":"in_range","right":["stock","dr","fund"]},{"left":"subtype","operation":"in_range","right":["common","","etf","unit","mutual","money","reit","trust"]}],"options":{"data_restrictions":"PREV_BAR","lang":"id_ID"},"symbols":{"query":{"types":[]},"tickers":[]},"columns":["name","close"],"sort":{"sortBy":"market_cap_basic","sortOrder":"desc"},"range":[0,300]}'  ## noqa

    print("Calling price API...")
    response = requests.post(url, payload).json()["data"]
    for content in response:
        info = content["d"]
        code = info[0]
        price = info[1]
        if code in data:
            data[code] = price

    return data


def scrape_save(date, data):
    if date not in dates:
        dates.append(date)
        write("dates", dates)

    for code, price in data.items():
        issuers[code]["prices"][date] = price
        write("issuers", issuers)

    return True


@streamlit.cache
def scrape_stockbit(token: str, pin: str):
    today = datetime.now().date().strftime("%Y-%m-%d")
    url = f"https://api.stockbit.com/v2.4/trade/report/trade_activity?start=1970-01-01&end={today}"
    headers = {
        "x-pin": pin,
        "authorization": f"Bearer {token}",
    }

    print("Calling Stockbit trade API...")
    return requests.get(url, headers=headers).json()["data"]["result"]
