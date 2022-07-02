# Perintis

Perintis (an inaccurate translation of Vanguard) is a tool to help your track and purchase Indonesian stocks using market indices and their respective weighing mechanism. Built with Streamlit.

## Installation instructions

1. Install [Pipenv](https://pypi.org/project/pipenv/).
2. Run `pipenv install`.
3. Copy `.env.example` to `.env`.
4. Log in to your Stockbit and brokerage account, then open browser console and run the following script. Copy the result to `.env`.

```
const token = localStorage.getItem("securitiesAccessToken");
`STOCKBIT_TOKEN=${token}`;
```

5. Optionally, if you have stocks in other broker, put them in a new file named `holdings.json` with this format:

```
{
    "<ticker>": {
        "shares": <number of shares in lots/multiple of 100)>,
        "value": <purchase value>
    }
}
```

6. Run `pipenv run streamlit run perintis.py`.

## FAQ

### How does stock weighting is calculated?

IDX30 is using free float market capitalization-based weighting, meaning a company with higher market cap will have more weight allocation. Market cap is calculated with 2 things: amount of free-floating shares and price.

1. Every few months, IDX is publishing index updates containing the list of companies and the number of free-floating market shares
2. Price is determined by calculating the average of daily closing price of the past month of each stocks. While not the most scientific approach, this is a good normalization approach as by its nature, market cap is determined by daily movements. By using average price, we are trying to minimize the fluctation.

## In development

1. Track indices other than IDX30.
