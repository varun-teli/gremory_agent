# app.py

from flask import Flask, request, jsonify
from utils.helpers import handle_input, handle_input_error
from engines.actionEngine import ActionEngine
from engines.dataCollectionEngine import DataCollectionEngine
from engines.rebalancer import Rebalancer
from config import Config
from utils.schemas import WebhookRequest
from pydantic import ValidationError

app = Flask(__name__)
app.config.from_object(Config)

# Engines
data_collector = DataCollectionEngine()
rebalancer = Rebalancer(data_collector)
action_engine = ActionEngine(rebalancer)  # Inject rebalancer

# Register actions
action_engine.register_action("deploy", lambda **kwargs: action_engine.deploy(kwargs.get("amount", Config.INITIAL_FUNDS)))
action_engine.register_action("get_position", lambda **kwargs: action_engine.get_position())
action_engine.register_action("price", lambda **kwargs: {"price": data_collector.get_price(kwargs.get("source", "live"))})
action_engine.register_action("stop_monitoring", lambda **kwargs: rebalancer.stop() or {"message": "Monitoring stopped."})

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        raw_data = request.get_json(force=True)
        data = WebhookRequest(**raw_data)
        return jsonify(handle_input(data.model_dump(), action_engine))
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/price", methods=["GET"])
def get_price():
    source = request.args.get("source", "live")
    return jsonify({"price": data_collector.get_price(source)})

@app.route("/position", methods=["GET"])
def position():
    return jsonify(action_engine.get_position())

@app.route("/stop_monitoring", methods=["POST"])
def stop_monitoring():
    rebalancer.stop()
    return jsonify({"message": "Monitoring stopped manually."})

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], host=app.config["HOST"], port=app.config["PORT"])
