import os, threading, time, random, requests
from flask import Flask, jsonify

app = Flask(__name__)
PLACE_ID = 109983668079237

best_lock = threading.Lock()
best = {"placeId": PLACE_ID, "jobId": None, "income": 0, "players": 0, "found_at": None}

def load_cookies():
    i,c=1,[]
    while os.environ.get(f"COOKIE_{i}"): c.append(os.environ.get(f"COOKIE_{i}")); i+=1
    print(f"LOADED {len(c)} COOKIES – CHAIN MODE")
    return c

COOKIES = load_cookies()

def scanner(cookie):
    s = requests.Session()
    s.cookies[".ROBLOSECURITY"] = cookie
    s.headers["User-Agent"] = "Roblox/WinInet"

    while True:
        try:
            cursor = ""
            while cursor is not None:
                r = s.get(f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/Public",
                          params={"sortOrder":"Asc","limit":100,"cursor":cursor or ""}, timeout=15)

                if r.status_code == 429:
                    time.sleep(random.uniform(60,90)); break
                if r.status_code != 200:
                    time.sleep(10); break

                data = r.json()
                for srv in data.get("data",[]):
                    p = srv["playing"]
                    if 4 <= p <= 15:                                 # ← REAL farming range again
                        income = p * 2200000
                        with best_lock:
                            if income > best["income"]:
                                joining = srv["id"]
                                best.update({"jobId":joining, "income":income, "players":p,
                                            "found_at":time.strftime("%H:%M:%S")})
                                print(f"★★★ JACKPOT → {income//1000000}M | {p}p | {joining}")

                                # Forget this server after 30 seconds so we chain to the next
                                threading.Timer(30, lambda: best.update({
                                    "jobId":None,"income":0,"players":0,"found_at":None
                                }) if best.get("jobId")==joining else None).start()

                cursor = data.get("nextPageCursor")
                time.sleep(1.4)
            time.sleep(random.uniform(22,38))
        except Exception as e:
            print("Error:",e); time.sleep(15)

@app.route("/latest")
def latest():
    with best_lock: return jsonify(best)

if __name__ == "__main__":
    print(f"STARTING {len(COOKIES)} THREADS – REAL JACKPOT CHAIN")
    for c in COOKIES:
        threading.Thread(target=scanner, args=(c,), daemon=True).start()
        time.sleep(1)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",8080)))
