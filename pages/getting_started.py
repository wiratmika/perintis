import streamlit

from core import get_stockbit_credentials


def app():
    credentials = get_stockbit_credentials()
    if not credentials[0] or not credentials[1]:
        streamlit.subheader(
            "Warning: Stockbit credentials are not set. Portfolio will not work."
        )

    streamlit.write(
        """
        ## How to use
        1. Fine-tune "Your capital" input on the sidebar until "Additional capital required" is near your intended value of stock purchases.
        2. Top-up your brokerage account with at least "Additional capital required" amount and some extra buffer for safety.
        3. Press "Purchase according to recommended allocation" and let the magic works.
        4. Carry on with your life until the next time you want to purchase stocks again; the beauty of index investing is that you don't have to think nor monitor about it, unlike active investing.

        By default, auto-buy will only purchase stocks whose diff is greater than 0. You may also manually adjust your holdings by sell stocks which price had gone up from your average purchase prices, indicated by negative diff.
        """
    )