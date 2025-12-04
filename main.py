import os
import threading
import time
import random
import requests
from flask import Flask, jsonify

app = Flask(__name__)
PLACE_ID = 109983668079237

best_lock = threading.Lock()
best = {"placeId": PLACE_ID, "jobId": None, "income": 0, "players": 0, "found_at": None}

def load_cookies():
    i, c = 1, []
    while True:
        cookie = os.environ.get(f"COOKIE_{i}")
        if not cookie: break
        c.append(cookie)
        i += 1
    print(f"LOADED {len(c)} ALTS – MAX 8P OPTIMIZED")
    return c

COOKIES = load_cookies()

def scanner(cookie):
    s = requests.Session()
    s.cookies[".ROBLOSECURITY"] = cookie
    s.headers["User-Agent"] = "Roblox/WinInet"
    while True:
        try:
            cursor = ""
            page = 0
            while cursor is not None:
                page += 1
                r = s.get(f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/Public",
                          params={"sortOrder": "Asc", "limit": 100, "cursor": cursor or ""}, timeout=12)

                if r.status_code == 429:
                    print("429 – sleeping 80s")
                    time.sleep(random.uniform(80, 110))
                    break
                if r.status_code != 200:
                    time.sleep(7)
                    break

                data = r.json()
                servers = data.get("data", [])
                good = sum(1 for x in servers if 4 <= x["playing"] <= 7)
                print(f"PAGE {page} – {len(servers)} servers – {good} in 4-7 range")

                for srv in servers:
                    p = srv["playing"]
                    if 4 <= p <= 7:  # OPTIMAL FOR MAX 8P – 8.8M to 15.4M income
                        income = p * 2200000
                        with best_lock:
                            if income > best["income"]:
                                joining = srv["id"]
                                best.update({"jobId": joining, "income": income, "players": p, "found_at": time.strftime("%H:%M:%S")})
                                print(f"JACKPOT → {income//1000000}M | {p}p | {joining}")
                                threading.Timer(20, lambda: best.update({"jobId": None, "income": 0, "players": 0})).start()

                cursor = data.get("nextPageCursor")
                time.sleep(1.1)
            time.sleep(random.uniform(15, 30))
        except Exception as e:
            print("Error:", e)
            time.sleep(10)

@app.route("/")
def home():
    return "scanner alive – max 8p mode"

@app.route("/latest")
def latest():
    with best_lock:
        return jsonify(best)

if __name__ == "__main__":
    print("MAX 8P SCANNER LIVE – 4-7P TARGETED")
    for c in COOKIES:
        threading.Thread(target=scanner, args=(c,), daemon=True).start()
        time.sleep(0.7)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=False, use_reloader=False)
