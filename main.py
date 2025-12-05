import os
import threading
import time
import random
import requests
import logging
from flask import Flask, jsonify

# KILL RED SPAM FOREVER
logging.getLogger("werkzeug").setLevel(logging.ERROR)

app = Flask(__name__)
PLACE_ID = 109983668079237

best_lock = threading.Lock()
best = {"placeId": PLACE_ID, "jobId": None, "income": 0, "players": 0, "found_at": None}

def load_cookies():
    cookies = [v.strip() for k, v in os.environ.items() if k.startswith("COOKIE_") and v.strip()]
    print(f"LOADED {len(cookies)} ALTS – FULL AGGRO MODE")
    return cookies

COOKIES = load_cookies()

def scanner(cookie):
    s = requests.Session()
    s.cookies[".ROBLOSECURITY"] = cookie
    s.headers["User-Agent"] = "Roblox/WinInet"
    
    while True:
        try:
            cursor = ""
            total_scanned = 0
            start_time = time.time()
            
            while cursor is not None:
                r = s.get(
                    f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/Public",
                    params={"limit": 100, "cursor": cursor},
                    timeout=7
                )
                if r.status_code != 200:
                    print(f"ALT {cookie[:10]}... → HTTP {r.status_code} – retrying")
                    time.sleep(1)
                    continue
                    
                data = r.json()
                servers = data.get("data", [])
                total_scanned += len(servers)
                
                # FORCE LOG EVERY PAGE – YOU WILL SEE THIS NON-STOP
                good = sum(1 for x in servers if 4 <= x["playing"] <= 7)
                print(f"SCANNING LIVE → {total_scanned} servers | {good} good (4-7p) | ALT {cookie[:12]}...")

                for srv in servers:
                    p = srv["playing"]
                    if 4 <= p <= 7:
                        income = p * 2200000
                        with best_lock:
                            if income > best["income"]:
                                joining = srv["id"]
                                best.update({"jobId": joining, "income": income, "players": p})
                                print(f"JACKPOT → {income//1000000}M | {p}p | {joining} ← TELEPORT NOW")
                                threading.Timer(12, lambda: best.update({"jobId": None, "income": 0, "players": 0})).start()

                cursor = data.get("nextPageCursor")
                time.sleep(0.3)  # MAXIMUM SPEED

            elapsed = time.time() - start_time
            print(f"FULL LIST SCANNED → {total_scanned} servers in {elapsed:.1f}s – restarting instantly")
            time.sleep(1)  # tiny breath

        except Exception as e:
            print("Scanner crashed:", e)
            time.sleep(2)

@app.route("/latest")
def latest():
    with best_lock:
        return jsonify(best)

if __name__ == "__main__":
    print("AGGRESSIVE SCANNER STARTED – LOGS EVERY 2–3 SECONDS")
    for i, c in enumerate(COOKIES):
        threading.Thread(target=scanner, args=(c,), daemon=True).start()
        print(f"ALT {i+1} STARTED")
    
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=False, use_reloader=False)
