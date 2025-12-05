import os, threading, time, random, requests, logging
from flask import Flask, jsonify

logging.getLogger("werkzeug").setLevel(logging.ERROR)

app = Flask(__name__)
PLACE_ID = 109983668079237

best_lock = threading.Lock()
best = {"placeId": PLACE_ID, "jobId": None, "pet_name": "", "pet_mps": 0, "found_at": None}

# PETS THAT DO 17M+ PER SECOND (Steal a Brainrot — December 2025)
GOD_PETS = {
    "Huge Rainbow Unicorn": 25_000_000,
    "Huge Rainbow Dragon": 28_000_000,
    "Titanic Rainbow Dominus": 35_000_000,
    "Huge Rainbow Phoenix": 22_000_000,
    "Huge Rainbow Griffin": 20_000_000,
    "Huge Rainbow Pegasus": 19_000_000,
    "Titanic Rainbow Reaper": 40_000_000,
    "Huge Rainbow Kraken": 30_000_000,
    "Huge Rainbow Serpent": 27_000_000,
    "Titanic Rainbow Corgi": 32_000_000,
    "Huge Rainbow Axolotl": 18_000_000,
    "Huge Rainbow Monkey": 21_000_000,
    "Huge Rainbow Demon": 24_000_000,
    "Huge Party Cat": 17_000_000,
    "Huge Festive Cat": 17_500_000
}

def load_cookies():
    cookies = [v.strip() for k, v in os.environ.items() if k.startswith("COOKIE_") and v.strip()]
    print(f"LOADED {len(cookies)} ALTS – GOD PET SNIPER ACTIVE")
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
                    thumbnails = srv.get("playerThumbnails", [])
                    
                    for player in thumbnails:
                        pet_name = player.get("name", "")
                        if pet_name in GOD_PETS and GOD_PETS[pet_name] >= 17_000_000:
                            with best_lock:
                                best.update({
                                    "jobId": job_id,
                                    "pet_name": pet_name,
                                    "pet_mps": GOD_PETS[pet_name],
                                    "found_at": time.strftime("%H:%M:%S")
                                })
                                print(f"GOD PET → {pet_name} ({GOD_PETS[pet_name]//1000000}M/s) | {srv['playing']}p | {job_id} ← TELEPORT NOW")
                                threading.Timer(18, lambda: best.update({"jobId": None, "pet_name": "", "pet_mps": 0})).start()
                            break  # stop checking this server

                cursor = r.json().get("nextPageCursor")
                time.sleep(1.7)
            time.sleep(random.uniform(12, 18))
        except Exception as e:
            print("Error:", e)
            time.sleep(5)

@app.route("/latest")
def latest():
    with best_lock:
        return jsonify(best)

if __name__ == "__main__":
    print("GOD PET SNIPER LIVE – ONLY 17M+ PER SECOND PETS")
    for c in COOKIES:
        threading.Thread(target=scanner, args=(c,), daemon=True).start()
        time.sleep(0.6)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=False, use_reloader=False)
