import time
from typing import Tuple

import requests

from core import get_stockbit_token


def purchase_holdings(data):
    result = []
    for datum in data:
        response = purchase_stockbit(
            get_stockbit_token(),
            datum["Ticker"],
            datum["Diff"],
            datum["Price"],
        )
        result.append(response)

    return result


def purchase_stockbit(stockbit_token: str, ticker: str, lots: int, price: int):
    url = f"https://api.stockbit.com/v2.4/trade/buy/{ticker}"
    headers = {
        "authorization": f"Bearer {stockbit_token}",
    }
    epoch_time_in_ms = int(time.time()) * 1000
    shares = lots * 100
    data = f'orderkey=W-BUY-{epoch_time_in_ms}&symbol={ticker}&price={price}&shares={shares}&boardtype=RG&gtc=1'

    print("Calling Stockbit buy API...")
    result = requests.post(url, data, headers=headers)
    return result.content
