import os
import threading
import time
import random
import requests
from flask import Flask, jsonify

app = Flask(__name__)

PLACE_ID = 109983668079237
MIN_INCOME = 10000000

best = {
    "placeId": PLACE_ID,
    "jobId": None,
    "income": 0,
    "players": 0,
    "found_at": None
}

def load_cookies():
    cookies = []
    i = 1
    while True:
        c = os.environ.get(f"COOKIE_{i}")
        if not c:
            break
        cookies.append(c.strip())
        i += 1
    print(f"LOADED {len(cookies)} COOKIES")
    return cookies

COOKIES = load_cookies()

def scanner(cookie):
    s = requests.Session()
    s.cookies[".ROBLOSECURITY"] = cookie
    s.headers["User-Agent"] = "Roblox/WinInet"
    while True:
        try:
            cursor = ""
            while cursor is not None:
                params = {"sortOrder": "Asc", "limit": 100}
                if cursor:
                    params["cursor"] = cursor
                r = s.get(f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/Public", params=params, timeout=10)
                if r.status_code != 200:
                    break
                data = r.json()
                for srv in random.sample(data.get("data", []), len(data.get("data", []))):
                    p = srv["playing"]
                    if 4 <= p <= 12:
                        income = p * 2_200_000
                        if income > best["income"]:
                            best.update({
                                "jobId": srv["id"],
                                "income": income,
                                "players": p,
                                "found_at": time.strftime("%H:%M:%S")
                            })
                            print(f"NEW BEST → {income//1000000}M | Players: {p} | {srv['id']}")
                cursor = data.get("nextPageCursor")
                time.sleep(0.6)
            time.sleep(random.uniform(8, 16))
        except Exception as e:
            print("Scanner error:", e)
            time.sleep(10)

@app.route("/")
def home():
    return "scanner running"

@app.route("/latest")
def latest():
    return jsonify(best)

# THIS PART STARTS EVERYTHING
if __name__ == "__main__":
    print(f"STARTING {len(COOKIES)} SCANNER THREADS...")
    for cookie in COOKIES:
        threading.Thread(target=scanner, args=(cookie,), daemon=True).start()
        time.sleep(0.7)

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), use_reloader=False)
