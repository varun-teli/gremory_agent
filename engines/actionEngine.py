# engines/actionEngine.py

import json
import os
from pathlib import Path
from config import Config
from engines.dataCollectionEngine import DataCollectionEngine

POSITION_FILE = Path(__file__).resolve().parent.parent / "position.json"

class ActionEngine:
    def __init__(self, rebalancer=None):
        self.actions = {}
        self.rebalancer = rebalancer  # Will be passed in from app.py

    def register_action(self, name, func):
        self.actions[name] = func

    def run_action(self, name, **kwargs):
        if name in self.actions:
            return self.actions[name](**kwargs)
        return {"error": f"Action '{name}' not found."}

    def deploy(self, amount):
        price = float(DataCollectionEngine().get_price("live"))
        width = price * (Config.BIN_WIDTH_PERCENT / 2)
        position = {
            "position_id": 1,
            "funds_deployed": amount,
            "current_range": [round(price - width, 2), round(price + width, 2)],
            "current_price": price,
            "fees_earned": 0.0,
            "total_rebalances": 0,
            "rebalance_history": []
        }
        self._save_position(position)
        print(f"💰 Deployed ${amount} at price ${price} with range {position['current_range']}")

        if self.rebalancer:
            self.rebalancer.start()
            print("▶️ Monitoring started after deploy.")
        return position

    def get_position(self):
        pos = self._load_position()
        if not pos:
            return {"message": "No position found."}
        history = pos.get("rebalance_history", [])[:3]
        return {**pos, "recent_rebalances": history}

    def _load_position(self):
        if not POSITION_FILE.exists():
            return None
        with open(POSITION_FILE, "r") as f:
            return json.load(f)

    def _save_position(self, position):
        with open(POSITION_FILE, "w") as f:
            json.dump(position, f, indent=2)

    def save_position_for_rebalancer(self, position):
        self._save_position(position)

    def load_position_for_rebalancer(self):
        return self._load_position()
