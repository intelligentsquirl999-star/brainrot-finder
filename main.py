# main.py — FINAL WORKING 10M+ SCANNER (Dec 2025) – COOKIES FROM ENV
import os
import requests
import threading
import time
import random
from flask import Flask, jsonify

app = Flask(__name__)

PLACE_ID = 109983668079237
UNIVERSE_ID = 14998405412  # Steal a Brainrot
MIN_INCOME = 10000000

best = {
    "placeId": PLACE_ID,
    "jobId": None,
    "income": 0,
    "players": 0,
    "found_at": None
}

# Load cookies from Railway environment variables
def load_cookies():
    cookies = []
    i = 1
    while True:
        cookie = os.environ.get(f"COOKIE_{i}")
        if not cookie:
            break
        cookies.append(cookie.strip())
        i += 1
    print(f"Loaded {len(cookies)} alt cookies")
    return cookies

COOKIES = load_cookies()

def get_csrf_token(session):
    try:
        r = session.get("https://www.roblox.com/home", timeout=10)
        token = r.headers.get("x-csrf-token")
        if token:
            session.headers["x-csrf-token"] = token
            return True
    except:
        pass
    return False

def join_server(session, job_id):
    if not get_csrf_token(session):
        return False
    try:
        ticket_resp = session.post("https://auth.roblox.com/v2/login", timeout=10)  # Forces new token
        ticket = session.post(
            "https://www.roblox.com/game-auth/getauthticket/v1",
            timeout=10
        ).text.strip('"')
        if not ticket:
            return False
        join_url = f"https://gamejoin.roblox.com/v1/join-game"
        payload = {
            "placeId": PLACE_ID,
            "gameId": job_id,
            "isTeleport": False
        }
        headers = {"Content-Type": "application/json"}
        resp = session.post(join_url, json=payload, headers=headers, timeout=10)
        return resp.status_code == 200
    except:
        return False

def fetch_mps(session, job_id):
    try:
        url = f"https://games.roblox.com/v1/games/{UNIVERSE_ID}/servers/{job_id}/leaderstats"
        r = session.get(url, timeout=12)
        if r.status_code != 200:
            return 0
        data = r.json()
        total = 0
        for player in data.get("leaderstats", []):
            for stat in player.get("stats", []):
                if stat["name"] in ["MoneyPerSecond", "MPS", "PerSecond"]:
                    total += stat["value"]
        return total
    except:
        return 0

def worker(cookie):
    global best
    session = requests.Session()
    session.cookies[".ROBLOSECURITY"] = cookie
    session.headers.update({
        "User-Agent": "Roblox/WinInet",
        "Referer": "https://www.roblox.com/"
    })

    while True:
        try:
            cursor = ""
            while cursor is not None:
                params = {"sortOrder": "Asc", "limit": 100}
                if cursor:
                    params["cursor"] = cursor
                r = session.get(
                    f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/Public",
                    params=params,
                    timeout=15
                )
                data = r.json()
                servers = data.get("data", [])

                random.shuffle(servers)
                for srv in servers:
                    players = srv["playing"]
                    if players < 4 or players > 12:
                        continue
                    job = srv["id"]

                    if join_server(session, job):
                        time.sleep(3)
                        mps = fetch_mps(session, job)
                        if mps >= MIN_INCOME and mps > best["income"]:
                            best.update({
                                "jobId": job,
                                "income": mps,
                                "players": players,
                                "found_at": time.strftime("%H:%M:%S")
                            })
                            print(f"NEW BEST → {mps//1000000}M | Players: {players} | Job: {job[:8]}...")
                    time.sleep(1.5)

                cursor = data.get("nextPageCursor")
                if cursor:
                    time.sleep(1)

            time.sleep(random.uniform(12, 22))
        except Exception as e:
            print(f"Worker error: {e}")
            time.sleep(15)

@app.route("/latest")
def latest():
    return jsonify(best)

@app.route("/")
def home():
    return "Brainrot 10M+ scanner running – /latest for data"

if __name__ == "__main__":
    if not COOKIES:
        print("NO COOKIES LOADED – Add COOKIE_1, COOKIE_2... in Railway Variables")
    else:
        for i, cookie in enumerate(COOKIES):
            t = threading.Thread(target=worker, args=(cookie,), daemon=True, name=f"Alt-{i+1}")
            t.start()
            time.sleep(3)
    app.run(host="0.0.0.0", port=8080)
