# engines/dataCollectionEngine.py

import random
import requests
from config import Config

class DataCollectionEngine:
    def __init__(self, current_price=105.0):
        self.current_price = current_price

    def get_price(self, source="simulated"):
        if source == "live":
            return self.get_live_price()
        return self.get_simulated_price()

    def get_live_price(self):
        try:
            response = requests.get(Config.LIVE_PRICE_API_URL, timeout=5)
            data = response.json()
            return round(float(data["data"]["So11111111111111111111111111111111111111112"]["price"]), 4)
        except Exception as e:
            raise RuntimeError(f"Live price fetch failed: {e}")


    def get_simulated_price(self):
        delta = random.uniform(-Config.PRICE_DELTA, Config.PRICE_DELTA)
        self.current_price = round(
            max(Config.PRICE_MIN, min(self.current_price + delta, Config.PRICE_MAX)), 2
        )
        return self.current_price
