import streamlit as st
from dotenv import load_dotenv

import getting_started, portfolio

load_dotenv()
st.set_page_config(page_title="Perintis", page_icon=":dollar:", layout="wide")

"# Perintis"

PAGES = {
    "Getting Started": getting_started,
    "Portfolio": portfolio,
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to:", list(PAGES.keys()))
page = PAGES[selection]
page.app()
