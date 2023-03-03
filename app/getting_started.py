import streamlit


def app():
    streamlit.write(
        """
        ## How to use
        1. Fine-tune "Your capital" input on the sidebar until "Additional capital required" is near your intended value of stock purchases.
        2. Top-up your brokerage account with at least "Additional capital required" amount, plus Rp10,000 for stamp duty.
        3. Press "Purchase according to recommended allocation" and let the magic works.
        4. Carry on with your life until the next time you want to purchase stocks again; the beauty of index investing is that you don't have to think about nor monitor it, unlike active investing.

        By default, auto-purchase will only purchase stocks that you should buy but not sell stocks that you should sell. You may also manually adjust your holdings by sell stocks which price had gone up from your average purchase prices, indicated by negative differences.
        """
    )
