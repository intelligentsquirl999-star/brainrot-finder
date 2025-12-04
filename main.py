# main.py — FIXED ALT BOT SCANNER FOR 10M+ MPS (Dec 2025)
import requests
import threading
import time
import random
import json

from flask import Flask, jsonify

app = Flask(__name__)

PLACE_ID = 109983668079237
UNIVERSE_ID = 14998405412  # Universe ID for Steal a Brainrot (confirm via API if needed)
MIN_INCOME = 10000000
best = {"placeId": PLACE_ID, "jobId": None, "income": 0, "players": 0, "found_at": None}

# Your alts (keep 5–10 for speed; rotate to avoid bans)
COOKIES = [
    "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_CAEaAhADIhsKBGR1aWQSEzU2NzcxODM0NTc0ODAwMjMwMjAoAw.aNkbeecnkAisU-nHQXHv6n7rrXhneSzZQg60bvkgfvQp-71Ok064rHLJXM3xX2rkpP3BXDyd9SDuCvyFZRH8YidANiL7kqKLKyFT-vClEGv-kos5n1JKjhRHeK2WmhtW5OA5VB_Zb5eshLTv_071wo7BXO1PDlyr8Sdi1JPjy8hSeJE97OhyzZaWoBmfsXcREBJuuqDSLlzWh91VwOh8C3MH57ApIgBMe-2ZBv0jcgvQ-nCHVqK0L8NrsSK9SO28BoWUpYmPmD5hxbb4_831ECHBoVxdGwRtdCsqg3InsTd5YWU47bxte3583QarKEEaJqLKVNoVP1kjZtfhoTTTP9-CsZnWYI_bSU8RiSdigox9MYY5zP8r5LBIs0Di2rReFs0-yPp7z0Fwwe28_ZTWsh_ZSX6EcNicXvcbGUdOnI2CfbU_",
    "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_CAEaAhADIhwKBGR1aWQSFDE3MzUyNDkzNTIxNjg1NTQ4MTQzKAM.EyZq1rb9_mZiCbVvH2UZn8WJjW5QBrqiaZXpDqeOZgvQEjiOk7jPAPz9LLt_gQUUZsZinV4cAgJUo45jlUMKAFmy7II4u8pZyn2b6QY5H_9znopwz5m3TZCBf4fM7cqz9cnSwbRl0AX-0ODA0GmYI63Cirl75B7nRdIo774yECbJe2hyZUcc5mZS-R8yIb5b3xrWtPkNdFc39oKLX_1l2AOYmY3NdNYybQCQ7-69w0YNbvbVRghodxERreK4I-z2SHtcJhJqAxBse4xXc8Bcae9rqpvb2f92rfy2QXZLoyNkiljLorc1mO_u3Xv9P7UJcIB-wBdgbTDH1NH4klmuvjnckLlOudOtoZTf6kFEBgvvqxbB7TePlBe3q7bGuYweiIMMjRzzeXuEVpXnUegGrr2KtU6XEe5yaFXJDIA41eoPZYz2",
    "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_CAEaAhADIhwKBGR1aWQSFDEzMDQ4NzMwNzY1NTM2NDM1MDA3KAM.3Sk3IjEasxvNW3LY32Lcfg0NXwqN3mqh085yDunkQ4tC-TzStgeHGvTQgvb9JMvAeCsqlkG9HpLR50bYbuxfdvRJXEPkuRutSTHth8Ma1ymwXQ6RZfOTvizu2Knj7Xpa8LgB5V4dQDTWxcYsSFNnrXfELsjNled088u-UTA-IgHvFcN1ej1ffuNaBGF4q1OB6NgEd43lLvQ46De-Ir-vdjlQQBDbhpGemkhAomh1SMnE--dQCkAJL5mo-KvgE0RcYrVVdXvuhBQgarOHRXGqWvsZvSiWbf5xajwfeJuA6EKeLYcfsaIz_92GmCe_lgAHGi1iph1IVg3Z2pLqltwmfir_o8vIEyWL0sP_5eqM26gXO_5LozeaT8N5DggOlah70YVVnkwZSCjpeGO7vLmOJ0KTqJo",
    "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_CAEaAhADIhsKBGR1aWQSEzE0MDMzODEyMjk3NjEwODg1NjQoAw.4hQdG2u6f985CqDZ2V7A1sVqAZDLA8E9E44KM-fODZbro6VjoMSq7OoeSqVTUnSDonDVUhLU6kXspgLEJRru6H7NEdcYh86DHbhMTQPTymomHJuFkOmpOUeOIKnBFyWdzxy9Mj0pU4pfPBOkr4kN9NdSFJEUnorWxC2G8BddO_V7SU45k7vWv7t9S0X4wtnCnFl2OOGS7g8QnxNbcc3LwLyAZaXa41hz01cPnecCh2BbC-y2zZp9FOM57TRizzvjq2mRfYrGGmQ_7t0hl5_i1oGefm98FOytvTizrgIlCY_8Vyk-mFDKSZvMT1zev8DOWDnmAud9ur4JFytH7YpkhQ4WUuLeKx4MKYzkPprvZR9pmT_kBIit38k_iz0ymQfLbkYo5W0-wFbhU5wVy5rr4KYpIkQ",
    "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_CAEaAhADIhwKBGR1aWQSFDE3Njg2NzY1MDA5NjI4Mjk0MzUzKAM.g1wJG_ItCQtTCcP_liYx8gny7K2FA_vKqKFZIglpLbJ3TcHDGL-b-pJzH6OGi43HhW_InenOIVwlCR-h_3tsWFgzrh6xINvShLWuguvzDn_CtmmD7zEVz_zWiLn-C_w3HvD6ubqHgwEqGcKWscW7YvwEcVxTrLqMZOWZyc76WJN3J2WG9Snf-Cam4c0KjWafKZ0JsxfW61K1LQNVD65pK5cpMxpG8Q8KhmydVT6iPeqVvKTvj8nfxT6bdOlaFw30DVwUO-basdAV8uoMEO7Wj45xItdiSHsHpuNYBNeMd-gvM0lsVsD7UbS8ik3XGgVu5e3blpPUPjuEdO9pBOUCjk97bNWEXwkJpp0oGtD9GlWBEQWKp4uXDanScC7l1N0FOBTe9GeospVzeZ5BsttYG13KkqY",
    # Add more alts here for faster scanning (up to 15)
]

def get_csrf_token(session):
    """Fetch X-CSRF-TOKEN for auth (required in 2025)"""
    try:
        r = session.get("https://www.roblox.com/home", timeout=10)
        csrf_match = r.text.split('meta name="csrf-token" content="')[1].split('"')[0] if 'csrf-token' in r.text else None
        if csrf_match:
            session.headers["X-CSRF-TOKEN"] = csrf_match
            return True
    except:
        pass
    return False

def join_server(session, job_id):
    """2025 join flow: Auth + join (replaces deprecated game-auth/join)"""
    if not get_csrf_token(session):
        return False
    try:
        # Step 1: Get auth ticket
        auth_url = f"https://www.roblox.com/game-auth/getauthticket/v1"
        auth_r = session.post(auth_url, data={"request": {"playerId": 1, "placeId": PLACE_ID}}, timeout=10)
        ticket = auth_r.json().get("ticket")

        if ticket:
            # Step 2: Join with ticket
            join_url = f"https://www.roblox.com/game-auth/join-server/v1/{UNIVERSE_ID}/{PLACE_ID}/{job_id}"
            join_data = {"authTicket": ticket}
            join_r = session.post(join_url, json=join_data, timeout=10)
            return join_r.status_code == 200
    except:
        pass
    return False

def fetch_mps(session, job_id):
    """Fetch real MPS from leaderboards (sum MoneyPerSecond stats)"""
    try:
        # Correct 2025 endpoint for player leaderboards after join
        lb_url = f"https://games.roblox.com/v1/games/{UNIVERSE_ID}/player-leaderboards?placeId={PLACE_ID}&jobId={job_id}&limit=100"
        lb_r = session.get(lb_url, timeout=10)
        data = lb_r.json()
        
        total_mps = 0
        for entry in data.get("data", []):
            for stat in entry.get("stats", []):
                if stat["name"] in ["MoneyPerSecond", "PerSecond", "MPS"]:  # Common stat names
                    total_mps += stat["value"]
        
        return total_mps
    except:
        return 0

def worker(cookie):
    global best
    session = requests.Session()
    session.cookies[".ROBLOSECURITY"] = cookie
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Content-Type": "application/json"
    })
    
    while True:
        try:
            # Fetch servers with pagination (scan 500+ per cycle)
            cursor = ""
            while cursor is not None:
                params = {"sortOrder": "Asc", "limit": 100, "cursor": cursor}
                r = session.get(f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/Public", params=params, timeout=15)
                servers = r.json().get("data", [])
                
                for srv in servers:
                    players = srv["playing"]
                    if players < 4 or players > 12:  # Target 4–12 player lobbies (stacked meta)
                        continue
                    
                    job = srv["id"]
                    print(f"[{threading.current_thread().name}] Scanning {job[:8]}... ({players} players)")
                    
                    # Real join
                    if join_server(session, job):
                        time.sleep(3)  # Wait for join to settle
                        mps = fetch_mps(session, job)
                        if mps >= MIN_INCOME and mps > best["income"]:
                            best = {
                                "placeId": PLACE_ID,
                                "jobId": job,
                                "income": mps,
                                "players": players,
                                "found_at": time.strftime("%H:%M:%S")
                            }
                            print(f"NEW BEST [{threading.current_thread().name}] → {mps//1000000}M MPS | Players: {players} | Job: {job}")
                        time.sleep(2)  # Avoid rate limits
                    else:
                        print(f"[{threading.current_thread().name}] Join failed for {job[:8]}")
                
                cursor = r.json().get("nextPageCursor")
                if cursor:
                    time.sleep(1)
            
            time.sleep(random.uniform(10, 20))  # Cycle delay
        except Exception as e:
            print(f"[{threading.current_thread().name}] Error: {e}")
            time.sleep(15)

@app.route("/latest")
def latest():
    return jsonify(best)

@app.route("/")
def home():
    return "Brainrot 10M+ MPS Scanner Active – /latest for best server"

if __name__ == "__main__":
    for i, c in enumerate(COOKIES):
        t = threading.Thread(target=worker, args=(c,), daemon=True, name=f"Alt-{i+1}")
        t.start()
        time.sleep(2)  # Stagger starts
    app.run(host="0.0.0.0", port=8080, debug=False)
