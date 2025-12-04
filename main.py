import os, threading, time, random, requests, logging
from flask import Flask, jsonify

logging.getLogger('werkzeug').setLevel(logging.ERROR)  # ← THIS KILLS THE RED SPAM

app = Flask(__name__)
PLACE_ID = 109983668079237

best_lock = threading.Lock()
best = {"placeId": PLACE_ID, "jobId": None, "income": 0, "players": 0, "found_at": None}

def load_cookies():
    i,c=1,[]
    while os.environ.get(f"COOKIE_{i}"): c.append(os.environ.get(f"COOKIE_{i}")); i+=1
    print(f"LOADED {len(c)} ALTS – 30M+ GOD MODE ACTIVE")
    return c

COOKIES = load_cookies()

def scanner(cookie):
    s = requests.Session()
    s.cookies[".ROBLOX"] = cookie
    s.headers["User-Agent"] = "Roblox/WinInet"

    while True:
        try:
            cursor = ""
            while cursor is not None:
                r = s.get(f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/Public",
                          params={"sortOrder":"Asc","limit":100,"cursor":cursor or ""}, timeout=13)

                if r.status_code == 429:
                    time.sleep(random.uniform(80,110)); break
                if r.status_code != 200:
                    time.sleep(8); break

                for srv in r.json().get("data", []):
                    p = srv["playing"]
                    if 13 <= p <= 15:  # ONLY 30M+ WHALE SERVERS
                        income = p * 2200000
                        with best_lock:
                            if income > best["income"]:
                                joining = srv["id"]
                                best.update({"jobId":joining, "income":income, "players":p,
                                            "found_at":time.strftime("%H:%M:%S")})
                                print(f"GOD SERVER → {income//1000000}M | {p}p | {joining}")

                                # Forget in 18 seconds → instant next god server
                                threading.Timer(18.0, lambda: best.update({
                                    "jobId":None,"income":0,"players":0,"found_at":None
                                })).start()

                cursor = r.json().get("nextPageCursor")
                time.sleep(1.2)
            time.sleep(random.uniform(18,32))
        except: time.sleep(10)

@app.route("/latest")
def latest():
    with best_lock: return jsonify(best)

if __name__ == "__main__":
    print("BRAINROT GOD SCANNER LIVE – 30M+ ONLY")
    for c in COOKIES:
        threading.Thread(target=scanner, args=(c,), daemon=True).start()
        time.sleep(0.8)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",8080)), use_reloader=False)
