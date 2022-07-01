from typing import Tuple

import requests

from core import get_stockbit_token


def purchase_holdings(data):
    result = []
    for datum in data:
        response = purchase_stockbit(
            get_stockbit_token(),
            datum["Symbol"],
            datum["Diff"],
            datum["Price"],
        )
        result.append(response)

    return result


def purchase_stockbit(credentials: Tuple[str, str], symbol: str, lots: int, price: int):
    url = f"https://api.stockbit.com/v2.4/trade/buy/{symbol}"
    headers = {
        "x-pin": credentials[1],
        "authorization": f"Bearer {credentials[0]}",
        "content-type": "multipart/form-data; boundary=----WebKitFormBoundaryqpVBY9Ecoklfrz45",
    }
    shares = lots * 100
    data = f'------WebKitFormBoundaryqpVBY9Ecoklfrz45\r\nContent-Disposition: form-data; name="price"\r\n\r\n{price}\r\n------WebKitFormBoundaryqpVBY9Ecoklfrz45\r\nContent-Disposition: form-data; name="shares"\r\n\r\n{shares}\r\n------WebKitFormBoundaryqpVBY9Ecoklfrz45\r\nContent-Disposition: form-data; name="boardtype"\r\n\r\nRG\r\n------WebKitFormBoundaryqpVBY9Ecoklfrz45\r\nContent-Disposition: form-data; name="tradeshare"\r\n\r\n0\r\n------WebKitFormBoundaryqpVBY9Ecoklfrz45\r\nContent-Disposition: form-data; name="gtc"\r\n\r\n1\r\n------WebKitFormBoundaryqpVBY9Ecoklfrz45--\r\n'  # noqa

    print("Calling Stockbit buy API...")
    result = requests.post(url, data, headers=headers)
    return result.content
