import os

import requests


def purchase_holdings(data):
    result = []
    for datum in data:
        response = purchase_stockbit(
            os.getenv("STOCKBIT_TOKEN"),
            os.getenv("STOCKBIT_PIN"),
            datum["Code"],
            datum["Diff"],
            datum["Price"],
        )
        result.append(response)

    return result


def purchase_stockbit(token: str, pin: str, code: str, lots: int, price: int):
    url = f"https://api.stockbit.com/v2.4/trade/buy/{code}"
    headers = {
        "x-pin": pin,
        "authorization": f"Bearer {token}",
        "content-type": "multipart/form-data; boundary=----WebKitFormBoundaryqpVBY9Ecoklfrz45",
    }
    shares = lots * 100
    data = f'------WebKitFormBoundaryqpVBY9Ecoklfrz45\r\nContent-Disposition: form-data; name="price"\r\n\r\n{price}\r\n------WebKitFormBoundaryqpVBY9Ecoklfrz45\r\nContent-Disposition: form-data; name="shares"\r\n\r\n{shares}\r\n------WebKitFormBoundaryqpVBY9Ecoklfrz45\r\nContent-Disposition: form-data; name="boardtype"\r\n\r\nRG\r\n------WebKitFormBoundaryqpVBY9Ecoklfrz45\r\nContent-Disposition: form-data; name="tradeshare"\r\n\r\n0\r\n------WebKitFormBoundaryqpVBY9Ecoklfrz45\r\nContent-Disposition: form-data; name="gtc"\r\n\r\n1\r\n------WebKitFormBoundaryqpVBY9Ecoklfrz45--\r\n'

    print("Calling Stockbit order API...")
    result = requests.post(url, data, headers=headers)
    return result.content
