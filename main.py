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

# LOAD EVERY ALT – NO LIMIT
def load_cookies():
    cookies = [v.strip() for k, v in os.environ.items() if k.startswith("COOKIE_") and v.strip()]
    print(f"LOADED {len(cookies)} ALTS – HYPER SPEED MODE ON")
    return cookies or ["dummy"]  # prevent empty list crash

COOKIES = load_cookies()

def scanner(cookie):
    s = requests.Session()
    s.cookies[".ROBLOSECURITY"] = cookie
    s.headers["User-Agent"] = "Roblox/WinInet"
    
    while True:
        try:
            cursor = ""
            while cursor is not None:
                r = s.get(
                    f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/Public",
                    params={"limit": 100, "cursor": cursor},
                    timeout=8
                )
                if r.status_code != 200:
                    time.sleep(2)
                    continue
                    
                data = r.json()
                servers = data.get("data", [])
                
                # FAST SCAN – only check 4–7 players
                for srv in servers:
                    p = srv["playing"]
                    if 4 <= p <= 7:
                        income = p * 2200000
                        with best_lock:
                            if income > best["income"]:
                                joining = srv["id"]
                                best.update({
                                    "jobId": joining,
                                    "income": income,
                                    "players": p,
                                    "found_at": time.strftime("%H:%M:%S")
                                })
                                print(f"FIRE JACKPOT → {income//1000000}M | {p}p | {joining}")
                                # Clear after 15s for instant next
                                threading.Timer(15, lambda: best.update({"jobId": None, "income": 0, "players": 0})).start()

                cursor = data.get("nextPageCursor")
                time.sleep(0.4)  # 5× FASTER THAN BEFORE
            time.sleep(random.uniform(3, 7))  # short break
        except:
            time.sleep(3)

@app.route("/latest")
def latest():
    with best_lock:
        return jsonify(best)

if __name__ == "__main__":
    print("HYPER SPEED SCANNER ACTIVE – FINDING SERVERS IN SECONDS")
    # Start ALL alts IMMEDIATELY
    for cookie in COOKIES:
        threading.Thread(target=scanner, args=(cookie,), daemon=True).start()
    
    # Super lightweight server
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=False, use_reloader=False)
