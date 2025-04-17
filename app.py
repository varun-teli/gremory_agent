# app.py

from flask import Flask, request, jsonify
from config import Config
from engines.engine import mainEngine
from utils.helpers import inputHandler, inputErrorHandler



app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("Received webhook data:", data)

    # some prompt input or a hourly run.
    # run ExecutionEngine
    intentObj = inputHandler(data)
    if intentObj == "Important":
        mainEngine()
    else:
        inputErrorHandler()

    # Respond back to sender
    return jsonify({"status": "received", "data": data}), 200

if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
