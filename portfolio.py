from math import floor

from data import holdings, indices, issuers


def calculate(index: str, date, capital: int):
    if holdings:
        owned_holdings = holdings
    else:
        owned_holdings = {}

    data = []
    index_period = date.strftime("%Y-%m")

    total_value = 0
    for code, issuer in issuers.items():
        price = issuer["prices"][date]
        value = indices[index][index_period][code] * price
        total_value += value

    for code, issuer in issuers.items():
        price = issuer["prices"][date]
        value = indices[index][index_period][code] * price
        percentage = value / total_value
        weighted_value = percentage * capital
        shares = weighted_value / price
        lots = floor(shares / 100)
        holding = owned_holdings.get(code, [])
        owned = 0
        owned_value = 0
        purchased_value = 0
        for i in holding:
            owned += i[0]
            owned_value += i[0] * price * 100
            purchased_value += i[0] * i[1] * 100

        expected_value = lots * 100 * price

        data.append(
            {
                "Code": code,
                "Price": price,
                "Lots": lots,
                "Diff": lots - owned,
                "Owned": owned,
                "Name": issuer["name"],
                "Percentage": percentage,
                "Ideal Value": capital * percentage,
                "Expected Value": expected_value,
                "Owned Value": owned_value,
                "Diff Value": expected_value - owned_value,
                "Purchased Value": purchased_value,
                "Spent": purchased_value * 1.00145,
            }
        )

    return data
