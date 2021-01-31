import os
from datetime import timedelta
from math import floor

from data import indices
from scraper import scrape_stocks, scrape_stockbit


def get_holdings():
    data = scrape_stockbit(get_stockbit_credentials())
    result = {}

    for day in data["trade"]:
        for activity in day["activity"]:
            symbol = activity["symbol"]
            lot = int(activity["lot"].replace(".0", ""))
            price = int(activity["price"])
            transaction = (lot, price)
            result.setdefault(symbol, []).append(transaction)

    for order in data["order"]:
        symbol = order["symbol"]
        lot = order["order_total"]
        price = order["price_order"]
        transaction = (lot, price)
        result.setdefault(symbol, []).append(transaction)

    return result


def calculate(index: str, date, capital: int):
    holdings = get_holdings()
    stocks = scrape_stocks()

    result = []
    active_index = get_latest_period_index(indices[index], date)
    total_market_cap = get_total_market_cap(active_index)

    for symbol in active_index.keys():
        price = stocks[symbol][1]
        constituent = active_index[symbol]
        market_cap = constituent[0] * constituent[1]
        percentage = market_cap / total_market_cap
        weighted_value = percentage * capital
        shares = weighted_value / price
        lots = floor(shares / 100)
        holding = holdings.get(symbol, [])
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
                "Symbol": symbol,
                "Price": price,
                "Diff": lots - owned,
                "Lots": lots,
                "Owned": owned,
                "Name": stocks[symbol][0],
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


def get_latest_period_index(index, date):
    index_period = date.strftime("%Y-%m")

    while index_period not in index:
        date = date - timedelta(days=30)
        index_period = date.strftime("%Y-%m")

    return index[index_period]


def get_total_market_cap(index):
    total_value = 0
    for constituent in index.values():
        total_value += constituent[0] * constituent[1]

    return total_value


def get_stockbit_credentials():
    token = os.getenv("STOCKBIT_TOKEN")
    pin = os.getenv("STOCKBIT_PIN")
    return (token, pin)
