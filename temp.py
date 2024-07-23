from time import sleep

import requests

from services.price_mouth import PriceMonthService
from services.transaction import TransactionsService
from services.user import UserService

user_service = UserService()
transaction_service = TransactionsService()
price_mouth_service = PriceMonthService()

users = user_service.get_users()

ativos = transaction_service.get_fiis_from_transactions(
    user_id=users[0]["_id"])

print(ativos)

all_prices = []

for ativo in ativos:
    print(ativo)
    exists = price_mouth_service.get_by_ativo(ativo)
    if exists is not None:
        print(f"Ativo já existe prices month")
        continue

    response = requests.get(
        url=f"https://www.alphavantage.co/query?apikey=C8F4NRWAQ4XOYNCA&function=TIME_SERIES_MONTHLY&symbol={ativo}.SAO")

    if 'Monthly Time Series' not in response.json():
        print(f"Error: {ativo}")
        continue

    prices_month = []
    prices = response.json()['Monthly Time Series']
    for month in prices:
        prices_month.append({
            "ano": month.split("-")[0],
            "mes": month.split("-")[1],
            "open": prices[month]["1. open"],
            "high": prices[month]["2. high"],
            "low": prices[month]["3. low"],
            "close": prices[month]["4. close"],
            "volume": prices[month]["5. volume"],
        })

    price_mouth_service.insert({
        "ativo": ativo,
        "valor_por_mes": prices_month
    })
    # sleep(10)
