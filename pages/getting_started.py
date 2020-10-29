import streamlit


def app():
    streamlit.write(
        """
        ## How to use
        1. Fetch latest stock prices using Price Scraper and press "Save scrape result".
        2. Fine-tune "Your capital" input on the sidebar until "Additional capital required" is near your intended value of stock purchases.
        3. Top-up your brokerage account with at least "Additional capital required" amount and some extra buffer for safety.
        4. Press "Purchase according to recommended allocation" and let the magic works.
        5. Carry on with your life until the next time you want to purchase stocks again; the beauty of index investing is that you don't have to think nor monitor about it, unlike active investing.

        By default, auto-buy will only purchase stocks whose diff is greater than 0. You may also manually adjust your holdings by sell stocks which price had gone up from your average purchase prices, indicated by negative diff.
        """
    )
