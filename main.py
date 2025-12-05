import os
import threading
import time
import random
import requests
import logging
from flask import Flask, jsonify

# THIS LINE KILLS ALL RED GET /latest SPAM FOREVER
logging.getLogger("werkzeug").setLevel(logging.ERROR)

app = Flask(__name__)
PLACE_ID = 109983668079237

best_lock = threading.Lock()
best = {"placeId": PLACE_ID, "jobId": None, "income": 0, "players": 0, "found_at": None}

def load_cookies():
    cookies = [v.strip() for k, v in os.environ.items() if k.startswith("COOKIE_") and v.strip()]
    print(f"LOADED {len(cookies)} ALTS – HYPER MODE ACTIVE")
    return cookies

COOKIES = load_cookies()

def scanner(cookie):
    s = requests.Session()
    s.cookies[".ROBLOSECURITY"] = cookie
    s.headers["User-Agent"] = "Roblox/WinInet"
    
    while True:
        try:
            cursor = ""
            scanned = 0
            while cursor is not None:
                r = s.get(
                    f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/Public",
                    params={"limit": 100, "cursor": cursor},
                    timeout=7
                )
                if r.status_code != 200:
                    time.sleep(1)
                    continue
                    
                data = r.json()
                servers = data.get("data", [])
                scanned += len(servers)
                
                # LOG EVERY SCAN SO YOU SEE IT WORKING
                good = sum(1 for x in servers if 4 <= x["playing"] <= 7)
                if good > 0:
                    print(f"SCANNING → {scanned} servers seen | {good} JACKPOTS (4-7p)")
                
                for srv in servers:
                    p = srv["playing"]
                    if 4 <= p <= 7:
                        income = p * 2200000
                        with best_lock:
                            if income > best["income"]:
                                joining = srv["id"]
                                best.update({"jobId": joining, "income": income, "players": p})
                                print(f"JACKPOT LOCKED → {income//1000000}M | {p}p | {joining}")
                                threading.Timer(14, lambda: best.update({"jobId": None, "income": 0, "players": 0})).start()

                cursor = data.get("nextPageCursor")
                time.sleep(0.35)  # MAX SPEED WITHOUT 429

            print(f"FINISHED FULL SCAN → {scanned} servers checked – restarting in 4s")
            time.sleep(random.uniform(4, 8))

        except Exception as e:
            print("Scanner temp error:", e)
            time.sleep(3)

@app.route("/latest")
def latest():
    with best_lock:
        return jsonify(best)

if __name__ == "__main__":
    print("HYPER SCANNER LIVE – YOU WILL SEE SCANNING LINES EVERY 5 SECONDS")
    for c in COOKIES:
        threading.Thread(target=scanner, args=(c,), daemon=True).start()
    
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=False, use_reloader=False)
