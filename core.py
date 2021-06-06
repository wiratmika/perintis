import os
from collections import defaultdict
from datetime import timedelta
from math import ceil, floor

import streamlit

from data import indices
from scraper import scrape_stocks, scrape_stockbit


def get_holdings():
    credentials = get_stockbit_credentials()
    if not (credentials[0] and credentials[1]):
        return {}

    data = scrape_stockbit(credentials)
    result = defaultdict(list)

    for day in data["trade"]:
        for activity in day["activity"]:
            transaction = {
                "is_buy": activity["command"] == "BUY",
                "lot": int(activity["lot"].replace(".0", "")),
                "price": int(activity["price"]),
            }
            result[activity["symbol"]].append(transaction)

    for order in data["order"]:
        transaction = {
            "is_buy": True,
            "lot": order["order_total"],
            "price": order["price_order"],
        }
        result[order["symbol"]].append(transaction)

    return result


def calculate(index: str, date, contribution: int):
    holdings = get_holdings()
    stocks = scrape_stocks()

    result = []
    active_index = get_latest_period_index(indices[index], date)
    total_market_cap = get_total_market_cap(active_index)
    total_current_value = 0

    capital = get_current_portfolio_value(active_index, stocks, holdings) + contribution

    for symbol in active_index.keys():
        price = stocks[symbol][1]
        constituent = active_index[symbol]
        market_cap = constituent[0] * constituent[1]
        percentage = market_cap / total_market_cap
        weighted_value = percentage * capital
        shares = weighted_value / price
        lots = floor(shares / 100)
        transactions = holdings.get(symbol, [])
        owned = 0
        owned_value = 0
        purchased_value = 0
        for transaction in transactions:
            if transaction["is_buy"]:
                owned += transaction["lot"]
                owned_value += transaction["lot"] * price * 100
                purchased_value += transaction["lot"] * transaction["price"] * 100
            else:
                owned -= transaction["lot"]
                owned_value -= transaction["lot"] * price * 100
                purchased_value -= (
                    transaction["lot"] * transaction["price"] * 100
                )  # TODO: really?

        total_current_value += owned_value
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
                "Average Price": purchased_value / owned / 100
                if owned
                else 0,  # TODO really?
            }
        )

    total_expected_value = 0
    capital_needed = 0
    for i in result:
        total_expected_value += i["Expected Value"]
        capital_needed += i["Diff Value"] if i["Diff Value"] > 0 else 0

    capital_needed *= 1.0015
    capital_needed = ceil(capital_needed)

    return {
        "stocks": result,
        "total_current_value": total_current_value,
        "total_expected_value": total_expected_value,
        "capital_needed": capital_needed,
    }


@streamlit.cache
def get_current_portfolio_value(active_index, stocks, holdings):
    total_value = 0

    for symbol in active_index.keys():
        price = stocks[symbol][1]
        transactions = holdings.get(symbol, [])
        owned_value = 0
        for transaction in transactions:
            if transaction["is_buy"]:
                owned_value += transaction["lot"] * price * 100
            else:
                owned_value -= transaction["lot"] * price * 100

        total_value += owned_value

    return total_value


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
