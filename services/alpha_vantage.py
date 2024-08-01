import os

import requests
from dotenv import load_dotenv


class AlphaVantageService:
    def __init__(self):
        load_dotenv()
        self._url = "https://www.alphavantage.co/query"
        self._apikey = os.getenv('API_KEY_ALPHA')

    def get_price_by_month(self, ticker):
        params = {
            "apikey": self._apikey,
            "function": "TIME_SERIES_MONTHLY",
            "symbol": ticker
        }

        response = requests.get(url=self._url, params=params, timeout=5000)

        return response.json()
