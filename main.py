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
    print(f"LOADED {len(cookies)} ALTS – SNIPER FULLY ARMED")
    return cookies

COOKIES = load_cookies()

def scanner(cookie):
    s = requests.Session()
    s.cookies[".ROBLOSECURITY"] = cookie
    s.headers["User-Agent"] = "Roblox/WinInet"
    
    while True:
        try:
            cursor = ""
            total_servers = 0
            while cursor is not None:
                r = s.get(f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/Public",
                          params={"limit":100,"cursor":cursor}, timeout=10)
                
                if r.status_code != 200:
                    print(f"ALT {cookie[:10]}... → HTTP {r.status_code} – retrying in 3s")
                    time.sleep(3)
                    continue
                    
                data = r.json()
                servers = data.get("data", [])
                total_servers += len(servers)
                
                # LOG EVERY PAGE
                print(f"SCANNING → {total_servers} servers checked so far | ALT {cookie[:12]}...")

                for srv in servers:
                    for player in srv.get("playerThumbnails", []):
                        name = player.get("name", "").strip()
                        if name in TARGET_PETS:
                            with best_lock:
                                best.update({"jobId": srv["id"], "pet_name": name})
                                print(f"TARGET PET FOUND → {name} | {srv['playing']}p | {srv['id']} ← TELEPORTING NOW")
                                threading.Timer(18, lambda: best.update({"jobId":None,"pet_name":""})).start()
                           

                cursor = data.get("nextPageCursor")
                time.sleep(1.4)
                
            print(f"FULL LIST SCANNED → {total_servers} servers | restarting in 8s")
            time.sleep(random.uniform(8, 12))
            
        except Exception as e:
            print("Scanner error:", e)
            time.sleep(5)

@app.route("/latest")
def latest():
    with best_lock: return jsonify(best)

if __name__ == "__main__":
    print("YOUR PET SNIPER STARTED – LOGS EVERY 2–3 SECONDS")
    for i, c in enumerate(COOKIES, 1):
        threading.Thread(target=scanner, args=(c,), daemon=True).start()
        print(f"ALT {i} LAUNCHED AND SCANNING")
        time.sleep(0.5)
    
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",8080)), debug=False, use_reloader=False)
