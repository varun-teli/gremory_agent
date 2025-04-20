# engines/rebalancer.py

import asyncio
import threading
from config import Config

class Rebalancer:
    def __init__(self, data_collector):
        from engines.actionEngine import ActionEngine
        self.running = False
        self.data_collector = data_collector
        self.thread = None
        self.action_engine = ActionEngine()
        self.position_loader = self.action_engine.load_position_for_rebalancer
        self.position_saver = self.action_engine.save_position_for_rebalancer

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=asyncio.run, args=(self._run(),))
            self.thread.daemon = True
            self.thread.start()
            print("✅ Rebalancer started.")

    def stop(self):
        if self.running:
            self.running = False
            print("🛑 Rebalancer stopped.")

    async def _run(self):
        while self.running:
            await asyncio.sleep(Config.REBALANCE_INTERVAL)
            self.check_and_rebalance()

    def check_and_rebalance(self):
        position = self.position_loader()
        if not position:
            print("⚠️ No position deployed. Rebalancer paused.")
            return

        try:
            live_price = float(self.data_collector.get_price("live"))
        except Exception as e:
            print(f"❌ Failed to get live price: {e}")
            return

        current_range = position["current_range"]

        if live_price < current_range[0] or live_price > current_range[1]:
            new_mid = live_price
            width = new_mid * (Config.BIN_WIDTH_PERCENT / 2)
            new_range = [round(new_mid - width, 2), round(new_mid + width, 2)]

            rebalance_entry = {
                "price": live_price,
                "range": new_range,
                "rebalance_number": position["total_rebalances"] + 1
            }

            history = position.get("rebalance_history", [])
            history = [rebalance_entry] + history[:4]

            position["current_price"] = new_mid
            position["current_range"] = new_range
            position["fees_earned"] += Config.REBALANCE_FEE
            position["total_rebalances"] += 1
            position["rebalance_history"] = history

            self.position_saver(position)

            print(f"\n🔁 Rebalance #{rebalance_entry['rebalance_number']}")
            print(f"Live Price      : ${live_price}")
            print(f"New Range       : {new_range}")
        else:
            print(f"✔️ Price ${live_price} within range {current_range}")
