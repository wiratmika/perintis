import os
from math import ceil

import pandas as pd
import streamlit as st

from data import dates
from exceptions import InvalidSessionException
from holding import purchase_holdings
from portfolio import calculate


def app():
    st.header("Portfolio")

    capital = get_capital()
    date = st.sidebar.selectbox("Price date", dates, index=len(dates) - 1)
    try:
        portfolio_result = calculate("IDX30", date, capital)
    except InvalidSessionException:
        st.write("Invalid Stockbit crendentials, please re-check.")
        return

    auto_buy(portfolio_result)

    currency_format = "Rp{:,.0f}"
    st.dataframe(
        pd.DataFrame(portfolio_result)
        .style.format(
            {
                "Price": "{:,}",
                "Percentage": "{:.2%}",
                "Ideal Value": currency_format,
                "Expected Value": currency_format,
                "Owned Value": currency_format,
                "Diff Value": currency_format,
                "Purchased Value": currency_format,
                "Spent": currency_format,
            }
        )
        .applymap(_diff_color, subset=["Diff"]),
        height=600,
    )

    summary(portfolio_result)


def get_capital():
    default_capital = int(os.getenv("DEFAULT_CAPITAL_AMOUNT", 100000000))
    return st.sidebar.number_input("Your capital", value=default_capital, step=1000000)


def auto_buy(portfolio_result):
    if st.button("Purchase according to recommended allocation"):
        filtered_portfolio = filter(lambda x: x["Diff"] != 0, portfolio_result)
        result = purchase_holdings(filtered_portfolio)
        if result:
            for i in result:
                st.write(i)
            st.write("Purchase data sucessfully saved! Please refresh this page.")


def summary(portfolio_result):
    value = 0
    spent = 0
    capital_needed = 0

    for i in portfolio_result:
        value += i["Expected Value"]
        spent += i["Spent"]
        capital_needed += i["Diff Value"] if i["Diff Value"] > 0 else 0

    st.sidebar.write(f"Expected portfolio value: **Rp{value:,}**")

    spent = ceil(spent)
    st.sidebar.write(f"Capital spent: **Rp{spent:,}**")

    capital_needed *= 1.00145
    capital_needed = ceil(capital_needed)
    st.sidebar.write(
        f"Additional capital required (including commission): **Rp{capital_needed:,}**"
    )


def _diff_color(val):
    if val > 0:
        color = "red"
    elif val < 0:
        color = "green"
    else:
        color = "black"
    return f"color: {color}"
