import os, threading, time, random, requests, datetime
from flask import Flask, jsonify

app = Flask(__name__)
PLACE_ID = 109983668079237
best = {"placeId": PLACE_ID, "jobId": None, "income": 0, "players": 0, "found_at": None}

def load_cookies():
    cookies = []
    i = 1
    while os.environ.get(f"COOKIE_{i}"): cookies.append(os.environ.get(f"COOKIE_{i}")); i += 1
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
                r = s.get(f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/Public", 
                          params={"sortOrder":"Asc","limit":100,"cursor":cursor or ""}, timeout=10)
                if r.status_code != 200: break
                data = r.json()
                for srv in data.get("data", []):
                    p = srv["playing"]
                    if 4 <= p <= 12:
                        income = p * 2_200_000
                        if income > best["income"]:
                            best.update({"jobId":srv["id"], "income":income, "players":p, "found_at":time.strftime("%H:%M:%S")})
                            print(f"NEW BEST → {income//1000000}M | {p} players | {srv['id']}")
                cursor = data.get("nextPageCursor")
                time.sleep(0.6)
            time.sleep(random.uniform(8,16))
        except Exception as e:
            print("Scanner error:", e)
            time.sleep(10)

@app.route("/"); return "scanner running"
@app.route("/latest"); return jsonify(best)

# THIS IS THE IMPORTANT PART
if __name__ == "__main__":
    print(f"STARTING {len(COOKIES)} SCANNER THREADS NOW...")
    for c in COOKIES:
        threading.Thread(target=scanner, args=(c,), daemon=True).start()
        time.sleep(0.7)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",8080)), use_reloader=False)
