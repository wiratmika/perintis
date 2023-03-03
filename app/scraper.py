import requests
import streamlit
from bs4 import BeautifulSoup

from exceptions import InvalidSessionException


def scrape_stocks():
    data = {}

    url = "https://scanner.tradingview.com/indonesia/scan"
    payload = '{"filter":[{"left":"market_cap_basic","operation":"nempty"},{"left":"type","operation":"in_range","right":["stock","dr","fund"]},{"left":"subtype","operation":"in_range","right":["common","","etf","unit","mutual","money","reit","trust"]}],"options":{"data_restrictions":"PREV_BAR","lang":"id_ID"},"symbols":{"query":{"types":[]},"tickers":[]},"columns":["name","close","description","market_cap_basic","dividend_yield_recent","price_earnings_ttm","sector"],"sort":{"sortBy":"market_cap_basic","sortOrder":"desc"},"range":[0,300]}'  ## noqa

    print("Calling price API...")
    response = requests.post(url, payload).json()["data"]
    for content in response:
        info = content["d"]
        ticker = info[0]
        price = info[1]
        name = info[2]
        market_cap = info[3]
        dividend_yield = info[4]
        pe_ratio = info[5]
        sector = info[6]
        data[ticker] = (name, price, market_cap, dividend_yield, pe_ratio, sector)

    return data


def scrape_stockbit_portfolio(stockbit_token: str):
    headers = {
        "authorization": f"Bearer {stockbit_token}",
    }

    url = f"https://trading.masonline.id/portfolio"
    print("Calling Stockbit portfolio API...")
    response = requests.get(url, headers=headers)

    if response.status_code == 401:
        raise InvalidSessionException

    return response.json()["data"]["result"]


def scrape_stockbit_order(stockbit_token: str):
    headers = {
        "authorization": f"Bearer {stockbit_token}",
    }

    url = f"https://trading.masonline.id/order/list?gtc=1"
    print("Calling Stockbit order API...")
    response = requests.get(url, headers=headers)

    if response.status_code == 401:
        raise InvalidSessionException

    return response.json()["data"]


@streamlit.cache_data
def get_indices(index):
    if index == "MSCI":
        return scrape_msci()

    indices_urls = {
        "IDXHIDIV20": "https://raw.githubusercontent.com/wiratmika/indonesia-stock-indices/main/idxhidiv20.json",
    }
    return requests.get(indices_urls[index]).json()

def scrape_msci():
    html = requests.get("https://app2.msci.com/eqb/custom_indexes/indonesia_performance.html").text
    soup = BeautifulSoup(html, "html.parser")
    result = {}
    for i in soup.find(id="D_constituents").table.tbody.find_all("tr"):
        ticker = i.find_all("td")[10].text[:-3]
        shares = int(i.find_all("td")[4].text.replace(",", ""))
        price = int(i.find_all("td")[2].text.replace(".00000", ""))

        result[ticker] = {
            "shares": shares,
            "price": price,
        }

    return result
