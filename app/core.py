import os
import json
from math import ceil, floor

import streamlit

from scraper import (
    get_indices,
    scrape_stockbit_order,
    scrape_stockbit_portfolio,
    scrape_stocks,
)


def get_holdings(stockbit_token):
    if not stockbit_token:
        return {}

    portfolio = scrape_stockbit_portfolio(stockbit_token)
    orders = scrape_stockbit_order(stockbit_token)
    open_orders = filter(lambda x: x["status"] == "OPEN", orders)
    result = {}

    for datum in portfolio:
        result[datum["symbol"]] = {
            "shares": datum["balance_lot"],
            "average_price": datum["price_average"],
        }

    for datum in open_orders:
        ticker = datum["symbol"]
        if ticker in result:
            result[ticker]["shares"] += datum["order_total"]
        else:
            result[ticker] = {
                "shares": datum["order_total"],
            }

    local_data = get_local_holdings()
    if not local_data:
        return result

    for ticker, holding in local_data.items():
        if ticker in result:
            result[ticker]["shares"] += holding["shares"]
            result[ticker]["average_price"] = min(result[ticker]["average_price"], holding["average_price"])
        else:
            result[ticker] = {
                "shares": holding["shares"],
                "average_price": holding["average_price"],
            }

    return result


def calculate(index: str, contribution: int, stockbit_token: str):
    holdings = get_holdings(stockbit_token)
    stocks = scrape_stocks()

    result = []
    active_index = get_indices(index)
    total_market_cap = get_total_market_cap(active_index)

    capital = get_portfolio_market_value(stocks, holdings, active_index) + contribution

    for ticker in active_index.keys():
        price = stocks[ticker][1]
        constituent = active_index[ticker]
        market_cap = constituent["shares"] * constituent["price"]
        percentage = market_cap / total_market_cap
        weighted_value = percentage * capital
        shares = weighted_value / price
        lots = floor(shares / 100)

        holding = holdings.get(
            ticker,
            {
                "shares": 0,
            },
        )
        owned = holding["shares"]
        owned_value = price * owned * 100
        expected_value = lots * 100 * price
        dividend_yield = stocks[ticker][3] / 100 if stocks[ticker][3] else 0

        result.append(
            {
                "Ticker": ticker,
                "Price": price,
                "Average Price": None,
                "Desired": lots,
                "Owned": owned,
                "Diff": lots - owned,
                "Weight": percentage,
                "Desired Value": expected_value,
                "Owned Market Value": owned_value,
                "Value Differences": expected_value - owned_value,
                "Dividend Yield": dividend_yield,
                "Weighted Yield": dividend_yield * percentage,
                "Expected Dividend": owned_value * dividend_yield,
                "P/E Ratio": stocks[ticker][4],
                "Sector": stocks[ticker][5],
            }
        )

    # Include non-index holdings in the result, but ignored for purchase
    non_index_tickers = holdings.keys() - active_index.keys()
    for ticker in non_index_tickers:
        price = stocks[ticker][1]
        holding = holdings[ticker]
        owned = holding["shares"]
        owned_value = price * owned * 100
        dividend_yield = stocks[ticker][3] / 100 if stocks[ticker][3] else 0

        result.append(
            {
                "Ticker": ticker,
                "Price": price,
                "Average Price": holding["average_price"] if "average_price" in holding else None,
                "Desired": 0,
                "Owned": owned,
                "Diff": 0,
                "Weight": 0,
                "Desired Value": 0,
                "Owned Market Value": owned_value,
                "Value Differences": -owned_value if "average_price" in holding and holding["average_price"] < price else 0,
                "Dividend Yield": dividend_yield,
                "Weighted Yield": dividend_yield * percentage,
                "Expected Dividend": owned_value * dividend_yield,
                "P/E Ratio": stocks[ticker][4],
                "Sector": stocks[ticker][5],
            }
        )

    total_current_value = 0
    total_expected_value = 0
    capital_needed = 0
    expected_dividend = 0
    for i in result:
        total_current_value += i["Owned Market Value"]
        total_expected_value += i["Desired Value"]
        capital_needed += i["Value Differences"] if i["Value Differences"] > 0 else 0
        expected_dividend += i["Expected Dividend"]

    requires_stamp_duty = capital_needed > 10000000
    capital_needed *= 1.001  # 0.10% brokerage commission
    capital_needed += 10000 if requires_stamp_duty else 0
    capital_needed = ceil(capital_needed)
    expected_dividend = floor(expected_dividend)
    average_yield = expected_dividend / total_current_value if total_current_value else 0

    return {
        "stocks": result,
        "total_current_value": total_current_value,
        "total_expected_value": total_expected_value,
        "capital_needed": capital_needed,
        "expected_dividend": expected_dividend,
        "average_yield": average_yield,
    }


@streamlit.cache
def get_portfolio_market_value(stocks, holdings, active_index):
    total_value = 0

    for ticker, holding in holdings.items():
        if ticker in active_index:
            price = stocks[ticker][1]
            total_value += holding["shares"] * 100 * price

    return total_value


def get_total_market_cap(index):
    total_value = 0
    for constituent in index.values():
        total_value += constituent["shares"] * constituent["price"]

    return total_value


def get_local_holdings():
    if not os.path.isfile("holdings.json"):
        return {}

    with open("holdings.json", "r") as holdings_file:
        holdings = json.load(holdings_file)

    return holdings
