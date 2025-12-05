import os, threading, time, random, requests, logging
from flask import Flask, jsonify

logging.getLogger("werkzeug").setLevel(logging.ERROR)

app = Flask(__name__)
PLACE_ID = 109983668079237

best_lock = threading.Lock()
best = {"placeId": PLACE_ID, "jobId": None, "income": 0, "players": 0, "found_at": None, "rare_pet": False}

# REALISTIC RARE PETS YOU CAN ACTUALLY FIND (Dec 2025)
# These spawn in public servers every few hours
RARE_PETS = {
    "Huge Party Cat", "Huge Party Dog", "Huge Festive Cat", "Huge Santa Paws",
    "Huge Pumpkin Cat", "Huge Scarecrow Cat", "Huge Cupcake", "Huge Elf Cat",
    "Huge Snowman", "Huge Reindeer", "Huge Gingerbread Cat", "Huge Present Cat",
    "Huge Ornament Cat", "Huge Rainbow Unicorn", "Huge Rainbow Cat", "Huge Rainbow Dog",
    "Huge Lucky Cat", "Huge Dragon", "Huge Dog", "Huge Cat", "Huge Pegasus",
    "Huge Angel Dog", "Huge Angel Cat", "Huge Demon", "Huge Grim Reaper"
}

def load_cookies():
    cookies = [v.strip() for k, v in os.environ.items() if k.startswith("COOKIE_") and v.strip()]
    print(f"LOADED {len(cookies)} ALTS – REALISTIC RARE SNIPER ACTIVE")
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
                          params={"limit": 100, "cursor": cursor}, timeout=10)
                if r.status_code != 200:
                    time.sleep(3)
                    continue

                for srv in r.json().get("data", []):
                    job_id = srv["id"]
                    p = srv["playing"]

                    # RARE PET CHECK — PRIORITY 1
                    thumbnails = srv.get("playerThumbnails", [])
                    for player in thumbnails:
                        pet_name = player.get("name", "")
                        if any(rare in pet_name for rare in RARE_PETS):
                            with best_lock:
                                best.update({"jobId": job_id, "income": 999999999, "players": p, "rare_pet": True})
                                print(f"RARE PET → {pet_name} | {p}p | {job_id} ← TELEPORTING NOW")
                                threading.Timer(18, lambda: best.update({"jobId": None, "income": 0, "rare_pet": False})).start()
                            break

                    # Normal 4–7 player jackpot
                    elif 4 <= p <= 7 and not best["rare_pet"]:
                        income = p * 2200000
                        with best_lock:
                            if income > best["income"]:
                                best.update({"jobId": job_id, "income": income, "players": p})
                                print(f"JACKPOT → {income//1000000}M | {p}p | {job_id}")
                                threading.Timer(18, lambda: best.update({"jobId": None, "income": 0})).start()

                cursor = r.json().get("nextPageCursor")
                time.sleep(1.7)
            time.sleep(random.uniform(12, 20))
        except: time.sleep(5)

@app.route("/latest")
def latest():
    with best_lock: return jsonify(best)

if __name__ == "__main__":
    print("REALISTIC RARE PET + JACKPOT SNIPER LIVE")
    for c in COOKIES:
        threading.Thread(target=scanner, args=(c,), daemon=True).start()
        time.sleep(0.6)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",8080)), debug=False, use_reloader=False)
