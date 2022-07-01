import pandas as pd
import streamlit as st

from holding import purchase_holdings
from core import calculate, get_stockbit_token


def app():
    st.header("Portfolio")

    contribution = st.sidebar.number_input("Top-up amount", value=1000000, step=100000)
    portfolio_result = calculate("IDX30", contribution)

    auto_buy(portfolio_result["stocks"])

    currency_format = "Rp{:,.0f}"
    st.dataframe(
        pd.DataFrame(portfolio_result["stocks"])
        .style.format(
            {
                "Price": "{:,}",
                "Percentage": "{:.2%}",
                "Ideal Value": currency_format,
                "Expected Value": currency_format,
                "Owned Value": currency_format,
                "Diff Value": currency_format,
                "Purchased Value": currency_format,
                "Average Price": currency_format,
                "Spent": currency_format,
            }
        )
        .applymap(_diff_color, subset=["Diff"]),
        height=600,
    )

    summary(portfolio_result)


def auto_buy(portfolio_result):
    credentials = get_stockbit_token()
    if not (credentials[0] and credentials[1]):
        st.write("Auto-purchase is not available do to missing or invalid credentials")
    elif st.button("Purchase according to recommended allocation"):
        filtered_portfolio = filter(lambda x: x["Diff"] > 0, portfolio_result)
        result = purchase_holdings(filtered_portfolio)
        if result:
            for i in result:
                st.write(i)
            st.write("Purchase data sucessfully saved! Please refresh this page.")


def summary(portfolio_result):
    st.sidebar.write(
        f"Current portfolio value: **Rp{portfolio_result['total_current_value']:,}**"
    )
    st.sidebar.write(
        f"Expected portfolio value: **Rp{portfolio_result['total_expected_value']:,}**"
    )
    st.sidebar.write(
        f"Additional capital required (including commission): **Rp{portfolio_result['capital_needed']:,}**"
    )


def _diff_color(val):
    if val > 0:
        color = "red"
    elif val < 0:
        color = "green"
    else:
        color = "black"
    return f"color: {color}"
