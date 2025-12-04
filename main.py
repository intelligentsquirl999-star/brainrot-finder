# main.py — ULTRA-MINIMAL TEST VERSION (will deploy 100%)
import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Scanner is ALIVE – cookies loaded: " + str(bool(os.environ.get("COOKIE_1")))

@app.route("/latest")
def latest():
    return jsonify({
        "placeId": 109983668079237,
        "jobId": None,
        "income": 0,
        "players": 0,
        "found_at": None
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
