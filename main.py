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

# LOAD EVERY SINGLE ALT – NO LIMIT
def load_cookies():
    cookies = []
    for key, value in os.environ.items():
        if key.startswith("COOKIE_") and value.strip():
            cookies.append(value.strip())
    print(f"LOADED {len(cookies)} ALTS SUCCESSFULLY – STARTING SEARCH NOW")
    return cookies

COOKIES = load_cookies()
if not COOKIES:
    print("ERROR: NO COOKIES FOUND – ADD COOKIE_1, COOKIE_2, etc.")

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
                url = f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/Public"
                params = {"sortOrder": "Asc", "limit": 100}
                if cursor: params["cursor"] = cursor
                
                r = s.get(url, params=params, timeout=10)
                if r.status_code != 200:
                    time.sleep(5)
                    continue
                    
                data = r.json()
                servers = data.get("data", [])
                good = sum(1 for srv in servers if 4 <= srv["playing"] <= 7)
                print(f"ALT SCANNED PAGE {page} → {len(servers)} servers | {good} good (4-7p)")

                for srv in servers:
                    p = srv["playing"]
                    if 4 <= p <= 7:
                        income = p * 2200000
                        with best_lock:
                            if income > best["income"]:
                                joining = srv["id"]
                                best.update({"jobId": joining, "income": income, "players": p, "found_at": time.strftime("%H:%M:%S")})
                                print(f"★★★ JACKPOT FOUND → {income//1000000}M | {p} players | {joining}")
                                # Auto-clear after 18s
                                threading.Timer(18, lambda: best.update({"jobId": None, "income": 0, "players": 0})).start()

                cursor = data.get("nextPageCursor")
                time.sleep(0.9)  # Fast scan
            time.sleep(random.uniform(8, 15))
        except Exception as e:
            print("Scanner error:", e)
            time.sleep(8)

@app.route("/latest")
def latest():
    with best_lock:
        return jsonify(best)

if __name__ == "__main__":
    print("MAX 8P SCANNER FULLY ACTIVE – SEARCHING RIGHT NOW")
    for cookie in COOKIES:
        threading.Thread(target=scanner, args=(cookie,), daemon=True).start()
        time.sleep(0.5)  # Instant start
    
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=False, use_reloader=False)
