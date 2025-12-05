import os, threading, time, random, requests, logging
from flask import Flask, jsonify

logging.getLogger("werkzeug").setLevel(logging.ERROR)

app = Flask(__name__)
PLACE_ID = 109983668079237

best_lock = threading.Lock()
best = {"placeId": PLACE_ID, "jobId": None, "pet_name": "", "found_at": None}

# YOUR EXACT LIST – TELEPORT ON ANY OF THESE
TARGET_PETS = {
    "La Vacca Saturno Saturnita", "Bisonte Giuppitere", "Karkerkar Kurkur",
    "Los Matteos", "Los Tralaleritos", "Las Tralaleritas", "Graipuss Medussi",
    "La Grande Combinasion", "Torrtuginni Dragonfruitini", "Pot Hotspot",
    "Las Vaquitas Saturnitas", "Chicleteira Bicicleteira", "Agarrini la Palini",
    "Dragon Cannelloni", "Los Combinasionas", "Los Hotspotsitos", "Esok Sekolah",
    "Nuclearo Dinossauro", "Sammyni Spyderini", "Blackhole Goat", "Dul Dul Dul"
}

def load_cookies():
    cookies = [v.strip() for k, v in os.environ.items() if k.startswith("COOKIE_") and v.strip()]
    print(f"LOADED {len(cookies)} ALTS – SNIPING YOUR PETS")
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
                        pet_name = player.get("name", "").strip()
                        if pet_name in TARGET_PETS:
                            with best_lock:
                                best.update({
                                    "jobId": job_id,
                                    "pet_name": pet_name,
                                    "found_at": time.strftime("%H:%M:%S")
                                })
                                print(f"YOUR PET FOUND → {pet_name} | {srv['playing']}p | {job_id} ← TELEPORTING NOW")
                                # Clear after 18s so it can find another
                                threading.Timer(18, lambda: best.update({"jobId": None, "pet_name": ""})).start()
                            break  # stop checking this server

                cursor = r.json().get("nextPageCursor")
                time.sleep(1.6)
            time.sleep(random.uniform(10, 18))
        except Exception as e:
            print("Error:", e)
            time.sleep(5)

@app.route("/latest")
def latest():
    with best_lock:
        return jsonify(best)

if __name__ == "__main__":
    print("YOUR PET SNIPER IS LIVE – TELEPORTING ON SIGHT")
    for c in COOKIES:
        threading.Thread(target=scanner, args=(c,), daemon=True).start()
        time.sleep(0.6)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",8080)), debug=False, use_reloader=False)
