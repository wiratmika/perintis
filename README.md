# Perintis

Perintis (an inaccurate translation of Vanguard) is a tool to help your track and purchase Indonesian stocks using market indices and their respective weighing mechanism. Built with Streamlit.

## Installation instructions

1. Install [Pipenv](https://pypi.org/project/pipenv/).
2. Run `pipenv install`.
3. Copy `.env.example` to `.env` and `data/holdings.yaml.example` to `holding.yaml`.
4. Fill `DEFAULT_CAPITAL_AMOUNT` in `.env` to your expected capital allocation in stocks, and `STOCKBIT_TOKEN` & `STOCKBIT_PIN` with credentials retrieved from Stockbit app.
5. Run `pipenv run streamlit run perintis.py`.

## In development

1. Track indices other than IDX30.
2. Better holdings input mechanism.
3. Add more documentations on other values.
