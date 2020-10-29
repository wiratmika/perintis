import os
from math import floor

from data import indices, issuers
from scraper import scrape_stockbit


def get_holdings():
    data = scrape_stockbit(os.getenv("STOCKBIT_TOKEN"), os.getenv("STOCKBIT_PIN"))
    result = {}

    for day in data["trade"]:
        for activity in day["activity"]:
            code = activity["symbol"]
            lot = int(activity["lot"].replace(".0", ""))
            price = int(activity["price"])
            transaction = (lot, price)
            result.setdefault(code, []).append(transaction)

    for order in data["order"]:
        code = order["symbol"]
        lot = order["order_total"]
        price = order["price_order"]
        transaction = (lot, price)
        result.setdefault(code, []).append(transaction)

    return result


def calculate(index: str, date, capital: int):
    holdings = get_holdings()

    result = []
    index_period = date.strftime("%Y-%m")
    index_list = indices[index][index_period]
    total_market_cap = get_total_market_cap(index_list)

    for code, issuer in issuers.items():
        price = issuer["prices"][date]
        index_constituent = index_list[code]
        market_cap = index_constituent[0] * index_constituent[1]
        percentage = market_cap / total_market_cap
        weighted_value = percentage * capital
        shares = weighted_value / price
        lots = floor(shares / 100)
        holding = holdings.get(code, [])
        owned = 0
        owned_value = 0
        purchased_value = 0
        for i in holding:
            owned += i[0]
            owned_value += i[0] * price * 100
            purchased_value += i[0] * i[1] * 100

        expected_value = lots * 100 * price

        result.append(
            {
                "Code": code,
                "Price": price,
                "Diff": lots - owned,
                "Lots": lots,
                "Owned": owned,
                "Name": issuer["name"],
                "Percentage": percentage,
                "Ideal Value": capital * percentage,
                "Expected Value": expected_value,
                "Owned Value": owned_value,
                "Diff Value": expected_value - owned_value,
                "Purchased Value": purchased_value,
                "Spent": purchased_value * 1.00145,
            }
        )

    return result


def get_total_market_cap(index):
    total_value = 0
    for code, issuer in issuers.items():
        index_constituent = index[code]
        value = index_constituent[0] * index_constituent[1]
        total_value += value

    return total_value
