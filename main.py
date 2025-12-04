import os
import threading
import time
import random
import requests
from flask import Flask, jsonify

app = Flask(__name__)

PLACE_ID = 109983668079237
MIN_INCOME = 8800000  # Lowered to 4 players min

best = {
    "placeId": PLACE_ID,
    "jobId": None,
    "income": 0,
    "players": 0,
    "found_at": None
}

def load_cookies():
    cookies = []
    i = 1
    while True:
        c = os.environ.get(f"COOKIE_{i}")
        if not c:
            break
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
            page_count = 0
            while cursor is not None:
                params = {"sortOrder": "Asc", "limit": 100}
                if cursor:
                    params["cursor"] = cursor
                r = s.get(f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/Public", params=params, timeout=8)
                if r.status_code != 200:
                    print(f"HTTP {r.status_code} error for cookie")
                    break
                data = r.json()
                servers = data.get("data", [])
                random.shuffle(servers)  # Faster random check
                checked = 0
                for srv in servers:
                    checked += 1
                    p = srv["playing"]
                    if 4 <= p <= 12:
                        income = p * 2_200_000
                        if income >= MIN_INCOME and income > best["income"]:
                            best.update({
                                "jobId": srv["id"],
                                "income": income,
                                "players": p,
                                "found_at": time.strftime("%H:%M:%S")
                            })
                            print(f"NEW BEST → {income//1000000}M | Players: {p} | ID: {srv['id']}")
                        print(f"Checked server: {p} players | Est: {income//1000000}M")  # Debug every good range
                print(f"Page {page_count + 1}: Checked {len(servers)} servers, found {checked} in range")
                page_count += 1
                cursor = data.get("nextPageCursor")
                time.sleep(0.3)  # Faster page delay
            print(f"Full scan done for cookie. Sleeping {random.uniform(5, 10)}s")
            time.sleep(random.uniform(5, 10))  # Faster full cycle
        except Exception as e:
            print(f"Scanner error: {e}")
            time.sleep(8)

@app.route("/")
def home():
    return "scanner running fast"

@app.route("/latest")
def latest():
    return jsonify(best)

if __name__ == "__main__":
    print(f"STARTING {len(COOKIES)} FAST SCANNER THREADS...")
    for i, cookie in enumerate(COOKIES):
        t = threading.Thread(target=scanner, args=(cookie,), daemon=True)
        t.start()
        print(f"Thread {i+1} started")
        time.sleep(0.5)  # Stagger less

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), use_reloader=False)
