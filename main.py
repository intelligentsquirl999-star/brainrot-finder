import os, threading, time, random, requests, logging
from flask import Flask, jsonify

# KILL RED SPAM
logging.getLogger("werkzeug").setLevel(logging.ERROR)

app = Flask(__name__)
PLACE_ID = 109983668079237

best_lock = threading.Lock()
best = {"placeId": PLACE_ID, "jobId": None, "income": 0, "players": 0, "found_at": None}

def load_cookies():
    cookies = [v.strip() for k, v in os.environ.items() if k.startswith("COOKIE_") and v.strip()]
    print(f"LOADED {len(cookies)} ALTS – BALANCED MODE (NO 429)")
    return cookies

COOKIES = load_cookies()

def scanner(cookie):
    s = requests.Session()
    s.cookies[".ROBLOSECURITY"] = cookie
    s.headers["User-Agent"] = "Roblox/WinInet"
    
    while True:
        try:
            cursor = ""
            total = 0
            while cursor is not None:
                r = s.get(
                    f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/Public",
                    params={"limit": 100, "cursor": cursor},
                    timeout=10
                )
                
                if r.status_code == 429:
                    print("429 detected – sleeping 45s")
                    time.sleep(random.uniform(45, 65))
                    break
                if r.status_code != 200:
                    time.sleep(3)
                    continue
                    
                data = r.json()
                servers = data.get("data", [])
                total += len(servers)
                
                good = sum(1 for x in servers if 4 <= x["playing"] <= 7)
                if good > 0 or random.random() < 0.1:  # log ~10% of pages + all good ones
                    print(f"SCAN → {total} servers | {good} good (4-7p)")

                for srv in servers:
                    p = srv["playing"]
                    if 4 <= p <= 7:
                        income = p * 2200000
                        with best_lock:
                            if income > best["income"]:
                                joining = srv["id"]
                                best.update({"jobId": joining, "income": income, "players": p})
                                print(f"JACKPOT → {income//1000000}M | {p}p | {joining}")
                                threading.Timer(18, lambda: best.update({"jobId": None, "income": 0, "players": 0})).start()

                cursor = data.get("nextPageCursor")
                time.sleep(1.8)  # PERFECT SPEED – ZERO 429s

            print(f"Full scan done ({total} servers) – resting 12s")
            time.sleep(random.uniform(10, 16))

        except Exception as e:
            print("Error:", e)
            time.sleep(5)

@app.route("/latest")
def latest():
    with best_lock: return jsonify(best)

if __name__ == "__main__":
    print("BALANCED SCANNER LIVE – NO 429, LOGS EVERY SCAN")
    for i, c in enumerate(COOKIES, 1):
        threading.Thread(target=scanner, args=(c,), daemon=True).start()
        time.sleep(0.6)  # staggered start
        print(f"ALT {i} STARTED")
    
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",8080)), debug=False, use_reloader=False)
