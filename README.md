# Perintis

![Screenshot of Perintis](https://raw.githubusercontent.com/wiratmika/perintis/main/screenshot.png "Perintis")

Perintis (an inaccurate Indonesian translation of [Vanguard](https://investor.vanguard.com/home), the inspiration for this work) is a tool to help you track, visualize, and purchase Indonesian stocks using market indices and their respective weighing mechanism. It works with [Stockbit](https://stockbit.com/) brokerage and is built with [Streamlit](https://streamlit.io/).

## Background

Indonesian mutual funds are notorious for having comparatively high expense ratios. The author hypothesizes that Indonesian stock market liquidity and personal asset ownership (excluding primary residence) are relatively low compared to more developed countries. It leads to a lack of competition between the fund providers, where most products are sold by bank agents, wealth managers, and insurance plans instead of being sold directly to consumers.

For example, one of Indonesia's top stock mutual funds (by assets under management or AUM) costs 3.06% annually, while an index fund costs 1.57%. Conversely, highly-developed markets such as the United States offer physically-replicating funds for as low as 0.03%.

That is a high margin, given that even for retail investors, typical fees for buying and selling stocks are 0.15% and 0.25%, respectively, including tax (note that Indonesia does not have a capital gain tax for domestic stocks; taxes are final during selling). Institutional investors and individual investors with high AUM may obtain even lower fees. Indonesian stock indices' constituents change only twice yearly at most, which implies that rebalancing does not happen too frequently.

Perintis attempts to bypass the fund manager middleman by allowing individual investors using Stockbit to form index-based stock portfolios without paying the additional expense ratio. It calculates which and how many stocks one should buy based on current portfolio holdings and target market capitalization weight. It also removes the need to buy multiple stocks individually and automatically purchases them using the available market price.

## Installation instructions

1. Run `docker build -t perintis .`.
2. Copy `.env.example` to `.env`.
3. Log in to your Stockbit and brokerage account, open the browser console, then run the following script. Copy the result to `.env`.

```
const token = localStorage.getItem("securitiesAccessToken");
`STOCKBIT_TOKEN=${token}`;
```

4. Optionally, if you have stocks in other brokers, put them in a new file named `holdings.json` with this format:

```
{
    "<ticker>": {
        "shares": <number of shares in lots/multiple of 100)>,
        "value": <purchase value>
    }
}
```

5. Run `docker-compose up`.

## FAQ

### How is stock weighting calculated?

Most Indonesian stock market indices use free-floating, market capitalization-based weighting, meaning a company with a higher market cap will have more weight allocation. Market cap is determined by the amount of free-floating shares and the share price.

1. Every few months, the Indonesia Stock Exchange publishes index updates containing the list of companies and the number of free-floating market shares.
2. Price is determined by calculating each stock's average daily closing price of the past month. We are trying to minimize portfolio turnover for smaller portfolios by using average approximation instead of the latest closing price.

### Is this tool safe to use?

Privacy is why this tool is open-sourced and can only be run locally. Instead of entering your credentials into an opaque app (which introduces the risks of data breach and privacy violations), you have to run it in your environment so that the credentials are guaranteed never to be stored or sent anywhere except to the brokerage.

I acknowledge that this is a highly technical tool requiring a certain degree of knowledge to use. However, instead of trying to commercialize this as a ready-to-use product, Indonesian brokerages should directly implement the concepts introduced by this tool. It will be safer privacy-wise and decrease complexity due to not needing complex integrations between it and the brokerages.

I am open to pro-bono collaboration and consulting; one of my personal goals is to democratize and increase financial accessibility for the average Indonesian. You may contact me by email at my GitHub username at Gmail. In the long term, I hope this introduces pressure on the (especially index) fund managers to reduce their expense ratios, rendering this tool and the concepts it introduced obsolete.
