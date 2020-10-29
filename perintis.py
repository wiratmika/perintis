import os
from datetime import datetime
from math import ceil

import pandas
import streamlit
from dotenv import load_dotenv

from data import dates
from holding import purchase_holdings
from portfolio import calculate
from scraper import scrape, scrape_save

load_dotenv()

"# Perintis"

"""
## How to use
1. Fetch latest stock prices using scraper below and press "Save scrape result".
2. Fine-tune "Your capital" input on the sidebar until "Additional capital required" is near your intended value of stock purchases.
3. Top-up your brokerage account with at least "Additional capital required" amount and some extra buffer for safety.
4. Press "Purchase according to recommendation" and let the magic works.
5. Carry on with your life until the next time you want to purchase stocks again; the beauty of index investing is that you don't have to think nor monitor about it, unlike active investing.

By default, auto-buy will only purchase stocks whose diff is greater than 0. You may also manually adjust your holdings by sell stocks which price had gone up from your average purchase prices, indicated by negative diff.
"""

default_capital = int(os.getenv("DEFAULT_CAPITAL_AMOUNT", 100000000))
capital = streamlit.sidebar.number_input(
    "Your capital", value=default_capital, step=1000000
)

date = streamlit.sidebar.selectbox("Price date", dates, index=len(dates) - 1)
portfolio_result = calculate("IDX30", date, capital)

hide_zero_diff = streamlit.sidebar.checkbox("Hide zero diff stocks")
buying_mode = streamlit.sidebar.checkbox("Buying mode")


def difference_color(val):
    if val > 0:
        color = "red"
    elif val < 0:
        color = "green"
    else:
        color = "black"
    return f"color: {color}"


currency_format = "Rp{:,.0f}"
non_zero_diff_result = filter(lambda x: x["Diff"] != 0, portfolio_result)
result_to_show = non_zero_diff_result if hide_zero_diff else portfolio_result

if not buying_mode:
    portfolio = (
        pandas.DataFrame(result_to_show)
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
        .applymap(difference_color, subset=["Diff"])
    )
else:
    portfolio = pandas.DataFrame(result_to_show).loc[:, "Code":"Diff"]

"## Portfolio"
portfolio

value = 0
spent = 0
additional_capital = 0
for i in portfolio_result:
    value += i["Expected Value"]
    spent += i["Spent"]
    additional_capital += i["Diff Value"] if i["Diff Value"] > 0 else 0

f"Expected portfolio value: **Rp{value:,}**"

spent = ceil(spent)
f"Capital spent : **Rp{spent:,}**"

additional_capital *= 1.00145
f"Additional capital required (excluding sales, including commission): **Rp{ceil(additional_capital):,}**"

if streamlit.button("Purchase according to recommendation"):
    result = purchase_holdings(non_zero_diff_result)
    if result:
        for i in result:
            i
        "Purchase data sucessfully saved! Please refresh this page."
    else:
        "Oops something happened, please check console."

"## Scraper"
scrape_result = scrape()
scrape_data = [{"Code": k, "Price": v} for k, v in scrape_result.items()]

scraper = pandas.DataFrame(scrape_data)
today = datetime.now().date()
f"Today is {today}"
scraper

if streamlit.button("Save scrape result"):
    if scrape_save(today, scrape_result):
        "Scrape result sucessfully saved! Please refresh this page."
    else:
        "Oops something happened, please check console."
