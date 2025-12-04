import os, threading, time, random, http.client, json
from flask import Flask, jsonify

app = Flask(__name__)
PLACE_ID = 109983668079237
best_lock = threading.Lock()
best = {"placeId": PLACE_ID, "jobId": None, "income": 0, "players": 0, "found_at": None}

def load_cookies():
    i = 1
    c = []
    while os.environ.get(f"COOKIE_{i}"):
        c.append(os.environ.get(f"COOKIE_{i}"))
        i += 1
    print(f"LOADED {len(c)} COOKIES – LIGHT MODE")
    return c

COOKIES = load_cookies()

def light_scanner(cookie):
    while True:
        try:
            conn = http.client.HTTPSConnection("games.roblox.com")
            cursor = ""
            while cursor is not None:
                conn.request("GET", f"/v1/games/{PLACE_ID}/servers/Public?limit=100&cursor={cursor}")
                data = json.loads(conn.getresponse().read())
                for s in data.get("data", []):
                    p = s["playing"]
                    if 1 <= p <= 20:
                        inc = p * 2200000
                        with best_lock:
                            if inc > best["income"]:
                                best.update({"jobId": s["id"], "income": inc, "players": p, "found_at": time.strftime("%H:%M:%S")})
                                print(f"JACKPOT → {inc//1000000}M | {p}p | {s['id']}")
                cursor = data.get("nextPageCursor", None) or None
                time.sleep(1.5)
            conn.close()
            time.sleep(random.uniform(20, 35))
        except:
            time.sleep(15)

@app.route("/latest")
def latest():
    with best_lock: return jsonify(best)

if __name__ == "__main__":
    print(f"STARTING {len(COOKIES)} LIGHT THREADS – NO MEMORY LEAK")
    for c in COOKIES:
        t = threading.Thread(target=light_scanner, args=(c,), daemon=True)
        t.start()
        time.sleep(0.8)   # gentle start
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
