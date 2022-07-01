import os
from collections import defaultdict
from datetime import timedelta
from math import ceil, floor

import streamlit

from scraper import scrape_stocks, scrape_stockbit, get_indices


def get_holdings():
    token = get_stockbit_token()
    if not token:
        return {}

    data = scrape_stockbit(token)
    result = {}

    # TODO: handle buy orders

    for datum in data["portfolio"]:
        result[datum["symbol"]] = {
            "shares": datum["balance_lot"],
            "value": datum["total"],
        }

    return result


def calculate(index: str, contribution: int):
    holdings = get_holdings()
    stocks = scrape_stocks()

    result = []
    active_index = get_indices()[index]
    total_market_cap = get_total_market_cap(active_index)
    total_current_value = 0

    capital = get_portfolio_market_value(stocks, holdings) + contribution

    for symbol in active_index.keys():
        price = stocks[symbol][1]
        constituent = active_index[symbol]
        market_cap = constituent["shares"] * constituent["price"]
        percentage = market_cap / total_market_cap
        weighted_value = percentage * capital
        shares = weighted_value / price
        lots = floor(shares / 100)

        holding = holdings.get(symbol, {
            "shares": 0,
            "value": 0,
        })
        owned = holding["shares"]
        owned_value = price * owned * 100
        purchased_value = holding["value"]
        total_current_value += holding["value"]
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
                "Average Price": purchased_value / owned / 100 if owned else 0
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
def get_portfolio_market_value(stocks, holdings):
    total_value = 0

    for symbol, holding in holdings.items():
        price = stocks[symbol][1]
        total_value += price * holding["shares"]

    return total_value


def get_total_market_cap(index):
    total_value = 0
    for constituent in index.values():
        total_value += constituent["shares"] * constituent["price"]

    return total_value


def get_stockbit_token():
    return os.getenv("STOCKBIT_TOKEN")
