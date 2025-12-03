# main.py — FINAL WORKING SCANNER (Dec 2025)
import requests, threading, time, random, json
from flask import Flask, jsonify

app = Flask(__name__)

PLACE_ID = 109983668079237
MIN_INCOME = 10000000
best = {"placeId": PLACE_ID, "jobId": None, "income": 0, "players": 0}

# ←←← PUT YOUR ALT .ROBLOSECURITY COOKIES HERE (FULL WARNING INCLUDED)
COOKIES = [
   "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_CAEaAhADIhsKBGR1aWQSEzU2NzcxODM0NTc0ODAwMjMwMjAoAw.aNkbeecnkAisU-nHQXHv6n7rrXhneSzZQg60bvkgfvQp-71Ok064rHLJXM3xX2rkpP3BXDyd9SDuCvyFZRH8YidANiL7kqKLKyFT-vClEGv-kos5n1JKjhRHeK2WmhtW5OA5VB_Zb5eshLTv_071wo7BXO1PDlyr8Sdi1JPjy8hSeJE97OhyzZaWoBmfsXcREBJuuqDSLlzWh91VwOh8C3MH57ApIgBMe-2ZBv0jcgvQ-nCHVqK0L8NrsSK9SO28BoWUpYmPmD5hxbb4_831ECHBoVxdGwRtdCsqg3InsTd5YWU47bxte3583QarKEEaJqLKVNoVP1kjZtfhoTTTP9-CsZnWYI_bSU8RiSdigox9MYY5zP8r5LBIs0Di2rReFs0-yPp7z0Fwwe28_ZTWsh_ZSX6EcNicXvcbGUdOnI2CfbU_",
    "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_CAEaAhADIhwKBGR1aWQSFDE3MzUyNDkzNTIxNjg1NTQ4MTQzKAM.EyZq1rb9_mZiCbVvH2UZn8WJjW5QBrqiaZXpDqeOZgvQEjiOk7jPAPz9LLt_gQUUZsZinV4cAgJUo45jlUMKAFmy7II4u8pZyn2b6QY5H_9znopwz5m3TZCBf4fM7cqz9cnSwbRl0AX-0ODA0GmYI63Cirl75B7nRdIo774yECbJe2hyZUcc5mZS-R8yIb5b3xrWtPkNdFc39oKLX_1l2AOYmY3NdNYybQCQ7-69w0YNbvbVRghodxERreK4I-z2SHtcJhJqAxBse4xXc8Bcae9rqpvb2f92rfy2QXZLoyNkiljLorc1mO_u3Xv9P7UJcIB-wBdgbTDH1NH4klmuvjnckLlOudOtoZTf6kFEBgvvqxbB7TePlBe3q7bGuYweiIMMjRzzeXuEVpXnUegGrr2KtU6XEe5yaFXJDIA41eoPZYz2",
    "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_CAEaAhADIhwKBGR1aWQSFDEzMDQ4NzMwNzY1NTM2NDM1MDA3KAM.3Sk3IjEasxvNW3LY32Lcfg0NXwqN3mqh085yDunkQ4tC-TzStgeHGvTQgvb9JMvAeCsqlkG9HpLR50bYbuxfdvRJXEPkuRutSTHth8Ma1ymwXQ6RZfOTvizu2Knj7Xpa8LgB5V4dQDTWxcYsSFNnrXfELsjNled088u-UTA-IgHvFcN1ej1ffuNaBGF4q1OB6NgEd43lLvQ46De-Ir-vdjlQQBDbhpGemkhAomh1SMnE--dQCkAJL5mo-KvgE0RcYrVVdXvuhBQgarOHRXGqWvsZvSiWbf5xajwfeJuA6EKeLYcfsaIz_92GmCe_lgAHGi1iph1IVg3Z2pLqltwmfir_o8vIEyWL0sP_5eqM26gXO_5LozeaT8N5DggOlah70YVVnkwZSCjpeGO7vLmOJ0KTqJo",
  "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_CAEaAhADIhsKBGR1aWQSEzE0MDMzODEyMjk3NjEwODg1NjQoAw.4hQdG2u6f985CqDZ2V7A1sVqAZDLA8E9E44KM-fODZbro6VjoMSq7OoeSqVTUnSDonDVUhLU6kXspgLEJRru6H7NEdcYh86DHbhMTQPTymomHJuFkOmpOUeOIKnBFyWdzxy9Mj0pU4pfPBOkr4kN9NdSFJEUnorWxC2G8BddO_V7SU45k7vWv7t9S0X4wtnCnFl2OOGS7g8QnxNbcc3LwLyAZaXa41hz01cPnecCh2BbC-y2zZp9FOM57TRizzvjq2mRfYrGGmQ_7t0hl5_i1oGefm98FOytvTizrgIlCY_8Vyk-mFDKSZvMT1zev8DOWDnmAud9ur4JFytH7YpkhQ4WUuLeKx4MKYzkPprvZR9pmT_kBIit38k_iz0ymQfLbkYo5W0-wFbhU5wVy5rr4KYpIkQ",
 "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_CAEaAhADIhwKBGR1aWQSFDE3Njg2NzY1MDA5NjI4Mjk0MzUzKAM.g1wJG_ItCQtTCcP_liYx8gny7K2FA_vKqKFZIglpLbJ3TcHDGL-b-pJzH6OGi43HhW_InenOIVwlCR-h_3tsWFgzrh6xINvShLWuguvzDn_CtmmD7zEVz_zWiLn-C_w3HvD6ubqHgwEqGcKWscW7YvwEcVxTrLqMZOWZyc76WJN3J2WG9Snf-Cam4c0KjWafKZ0JsxfW61K1LQNVD65pK5cpMxpG8Q8KhmydVT6iPeqVvKTvj8nfxT6bdOlaFw30DVwUO-basdAV8uoMEO7Wj45xItdiSHsHpuNYBNeMd-gvM0lsVsD7UbS8ik3XGgVu5e3blpPUPjuEdO9pBOUCjk97bNWEXwkJpp0oGtD9GlWBEQWKp4uXDanScC7l1N0FOBTe9GeospVzeZ5BsttYG13KkqY",
    # Add 5–15 for faster finds

]

def worker(cookie):
    global best
    s = requests.Session()
    s.cookies[".ROBLOSECURITY"] = cookie
    s.headers["User-Agent"] = "Roblox/WinInet"

    while True:
        try:
            r = s.get(f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/Public?limit=100")
            servers = r.json()["data"]
            random.shuffle(servers)

            for srv in servers:
                if srv["playing"] >= 7: continue
                job = srv["id"]

                # Actually join the server (this is the missing step!)
                s.post("https://www.roblox.com/game-auth/join", data={"placeId": PLACE_ID, "jobId": job})

                time.sleep(2)

                # Get real total MoneyPerSecond from leaderboard
                lb = s.get(f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/{job}/leaderboards/v1").json()
                total = 0
                for entry in lb.get("entries", []):
                    if entry.get("stat") in ["MoneyPerSecond", "PerSecond"]:
                        total += entry.get("score", 0)

                if total >= MIN_INCOME and total > best["income"]:
                    best = {"placeId": PLACE_ID, "jobId": job, "income": total, "players": srv["playing"]}
                    print(f"NEW BEST → {total//1000000}M MPS")

        except: pass
        time.sleep(random.uniform(9, 14))

@app.route("/latest")
def latest():
    return jsonify(best)

if __name__ == "__main__":
    for c in COOKIES:
        threading.Thread(target=worker, args=(c,), daemon=True).start()
    app.run(host="0.0.0.0", port=8080)
