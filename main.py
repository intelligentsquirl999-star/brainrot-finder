import os, threading, time, random, requests
from flask import Flask, jsonify

app = Flask(__name__)
PLACE_ID = 109983668079237

best_lock = threading.Lock()
best = {"placeId": PLACE_ID, "jobId": None, "income": 0, "players": 0}

def load_cookies():
    cookies = [v.strip() for k,v in os.environ.items() if k.startswith("COOKIE_") and v.strip()]
    print(f"LOADED {len(cookies)} ALTS - LOW PLAYER SNIPER")
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
                r = s.get(f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/Public",
                          params={"limit":100,"cursor":cursor}, timeout=10)
                if r.status_code != 200: time.sleep(3); continue
                for srv in r.json().get("data",[]):
                    if 3 <= srv["playing"] <= 6:
                        income = srv["playing"] * 2200000
                        with best_lock:
                            if income > best["income"]:
                                best.update({"jobId":srv["id"],"income":income,"players":srv["playing"]})
                                print(f"LOW PLAYER SERVER → {income//1000000}M | {srv['playing']}p | {srv['id']}")
                cursor = r.json().get("nextPageCursor")
                time.sleep(2.2)
            time.sleep(15)
        except: time.sleep(5)

@app.route("/latest")
def latest(): 
    with best_lock: return jsonify(best)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",8080)), debug=False, use_reloader=False)
