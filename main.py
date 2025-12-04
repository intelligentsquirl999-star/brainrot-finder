import os, threading, time, random, requests
from flask import Flask, jsonify

app = Flask(__name__)
PLACE_ID = 109983668079237

best_lock = threading.Lock()
best = {"placeId": PLACE_ID, "jobId": None, "income": 0, "players": 0, "found_at": None}

def load_cookies():
    cookies = []
    i = 1
    while True:
        c = os.environ.get(f"COOKIE_{i}")
        if not c: break
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
                if cursor: params["cursor"] = cursor
                
                r = s.get(f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/Public", params=params, timeout=15)
                
                if r.status_code == 429:
                    print("429 → sleeping 50s")
                    time.sleep(random.uniform(50, 75))
                    break
                if r.status_code != 200: 
                    time.sleep(10)
                    break
                    
                data = r.json()
                servers = data.get("data", [])
                good = 0
                for srv in servers:
                    p = srv["playing"]
                    if 4 <= p <= 14:
                        income = p * 2200000
                        with best_lock:
                            # Auto-reset old dead server
                            if best["jobId"] and best["income"] > 0:
                                try:
                                    check = requests.get(f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/Public/{best['jobId']}", timeout=5).json()
                                    if check.get("playing", 0) == 0:
                                        best.update({"jobId": None, "income": 0, "players": 0, "found_at": None})
                                        print("Cleared dead server")
                                except: pass
                            # New best
                            if income > best["income"]:
                                best.update({"jobId": srv["id"], "income": income, "players": p, "found_at": time.strftime("%H:%M:%S")})
                                print(f"FRESH JACKPOT → {income//1000000}M | {p} players | {srv['id']}")
                        good += 1
                print(f"Scanned → {len(servers)} servers | {good} good")
                cursor = data.get("nextPageCursor")
                time.sleep(1.7)
            time.sleep(random.uniform(28, 45))
        except Exception as e:
            print("Error:", e)
            time.sleep(15)

@app.route("/")
def home(): return "scanner running"

@app.route("/latest")
def latest():
    with best_lock:
        return jsonify(best)

if __name__ == "__main__":
    print(f"STARTING {len(COOKIES)} THREADS – FINAL AUTO-CLEAR VERSION")
    for c in COOKIES:
        threading.Thread(target=scanner, args=(c,), daemon=True).start()
        time.sleep(1.8)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), use_reloader=False)
