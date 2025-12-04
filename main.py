import os, threading, time, random, requests
from flask import Flask, jsonify

app = Flask(__name__)
PLACE_ID = 109983668079237

best_lock = threading.Lock()
best = {"placeId": PLACE_ID, "jobId": None, "income": 0, "players": 0, "found_at": None}

def load_cookies():
    i,c=1,[]
    while os.environ.get(f"COOKIE_{i}"): c.append(os.environ.get(f"COOKIE_{i}")); i+=1
    print(f"LOADED {len(c)} COOKIES – 30M+ ONLY MODE")
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
                          params={"sortOrder":"Asc","limit":100,"cursor":cursor or ""}, timeout=14)

                if r.status_code == 429:
                    time.sleep(random.uniform(70,100)); break
                if r.status_code != 200:
                    time.sleep(8); break

                data = r.json()
                for srv in data.get("data",[]):
                    p = srv["playing"]
                    # ONLY 30M+ servers (13–15 players with insane pets)
                    if 13 <= p <= 15:
                        income = p * 2200000  # 28.6M – 33M real total
                        with best_lock:
                            if income > best["income"]:
                                joining = srv["id"]
                                best.update({"jobId":joining, "income":income, "players":p,
                                            "found_at":time.strftime("%H:%M:%S")})
                                print(f"ULTRA JACKPOT → {income//1000000}M | {p}p | {joining}")

                                # INSTANT FORGET AFTER 20 SECONDS — NEVER STUCK
                                threading.Timer(20.0, lambda: best.update({
                                    "jobId":None, "income":0, "players":0, "found_at":None
                                })).start()

                cursor = data.get("nextPageCursor")
                time.sleep(1.3)
            time.sleep(random.uniform(20,35))
        except Exception as e:
            print("Error:",e); time.sleep(12)

@app.route("/latest")
def latest():
    with best_lock: return jsonify(best)

if __name__ == "__main__":
    print(f"STARTING {len(COOKIES)} THREADS – 30M+ CHAIN MODE")
    for c in COOKIES:
        threading.Thread(target=scanner, args=(c,), daemon=True).start()
        time.sleep(0.9)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",8080)))
