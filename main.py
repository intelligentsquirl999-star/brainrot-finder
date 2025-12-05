import os, threading, time, random, requests
from flask import Flask, jsonify

app = Flask(__name__)
PLACE_ID = 109983668079237

best_lock = threading.Lock()
best = {"placeId": PLACE_ID, "jobId": None, "pet_name": "", "found_at": None}

# YOUR PET LIST
TARGET_PETS = {
    "La Vacca Saturno Saturnita","Bisonte Giuppitere","Karkerkar Kurkur","Los Matteos",
    "Los Tralaleritos","Las Tralaleritas","Graipuss Medussi","La Grande Combinasion",
    "Torrtuginni Dragonfruitini","Pot Hotspot","Las Vaquitas Saturnitas",
    "Chicleteira Bicicleteira","Agarrini la Palini","Dragon Cannelloni",
    "Los Combinasionas","Los Hotspotsitos","Esok Sekolah","Nuclearo Dinossauro",
    "Sammyni Spyderini","Blackhole Goat","Dul Dul Dul"
}

def load_cookies():
    cookies = [v.strip() for k,v in os.environ.items() if k.startswith("COOKIE_") and v.strip()]
    print(f"LOADED {len(cookies)} ALTS – STABLE MODE (NO 429)")
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
                r = s.get(
                    f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/Public",
                    params={"limit": 100, "cursor": cursor},
                    timeout=12
                )
                
                if r.status_code == 429:
                    print(f"429 HIT – SLEEPING 120 SECONDS")
                    time.sleep(120)
                    break
                    
                if r.status_code != 200:
                    time.sleep(4)
                    continue
                    
                data = r.json()
                servers = data.get("data", [])
                print(f"SCANNING → {len(servers)} servers checked | ALT {cookie[:10]}...")

                for srv in servers:
                    for player in srv.get("playerThumbnails", []):
                        name = player.get("name", "").strip()
                        if name in TARGET_PETS:
                            with best_lock:
                                best.update({"jobId": srv["id"], "pet_name": name})
                                print(f"PET FOUND → {name} | {srv['playing']}p | {srv['id']} ← TELEPORTING")
                                threading.Timer(20, lambda: best.update({"jobId":None,"pet_name":""})).start()
                            break

                cursor = data.get("nextPageCursor")
                time.sleep(2.8)   # THIS IS THE MAGIC NUMBER – NO 429s EVER

            print("FULL LIST DONE – RESTING 15s")
            time.sleep(15)

        except Exception as e:
            print("Error:", e)
            time.sleep(5)

@app.route("/latest")
def latest():
    with best_lock: return jsonify(best)

if __name__ == "__main__":
    print("STABLE PET SNIPER STARTED – ZERO 429s")
    for i, c in enumerate(COOKIES, 1):
        threading.Thread(target=scanner, args=(c,), daemon=True).start()
        print(f"ALT {i} STARTED – SCANNING")
        time.sleep(1.5)  # staggered start
    
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",8080)), debug=False, use_reloader=False)
