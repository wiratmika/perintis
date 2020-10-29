from datetime import datetime

import pandas as pd
import streamlit as st

from scraper import scrape, scrape_save


def app():
    st.header("Price Scraper")
    today = datetime.now().date()
    scrape_result = scrape()
    scrape_data = [{"Code": k, "Price": v} for k, v in scrape_result.items()]

    st.write(pd.DataFrame(scrape_data))
    st.write(f"Today is {today}")

    if st.button("Save scrape result"):
        scrape_save(today, scrape_result)
        st.write("Scrape result sucessfully saved! Please refresh this page.")
