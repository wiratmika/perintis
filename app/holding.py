import time

import requests

from core import get_stockbit_token


def purchase_holdings(data):
    result = []
    for offset, datum in reversed(list(enumerate(data))):
        response = purchase_stockbit(
            get_stockbit_token(),
            datum["Ticker"],
            datum["Diff"],
            datum["Price"],
            offset,
        )
        result.append(response)

    return result


def purchase_stockbit(
    stockbit_token: str, ticker: str, lots: int, price: int, offset: int
):
    url = f"https://trading.masonline.id/order/buy"
    headers = {
        "Authorization": f"Bearer {stockbit_token}",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    }
    epoch_time_in_ms = int(time.time()) * 1000
    epoch_time_in_ms -= offset
    shares = lots * 100
    data = f"orderkey=W-BUY-{epoch_time_in_ms}&symbol={ticker}&price={price}&shares={shares}&boardtype=RG&gtc=0"

    print("Calling Stockbit buy API...")
    result = requests.post(url, data, headers=headers)
    return result.content
