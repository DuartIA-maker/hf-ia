from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

API_KEY = "810bc8056a3c4df2bcdb3ffa1e9383f9"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/value-bets")
def value_bets():
    url = "https://api.football-data.org/v4/matches"
    headers = {"X-Auth-Token": API_KEY}

    response = requests.get(url, headers=headers)
    data = response.json()

    jogos = []

    for m in data["matches"][:5]:
        home = m["homeTeam"]["name"]
        away = m["awayTeam"]["name"]

        # EXEMPLO SIMPLES (depois melhoramos)
        prob = 0.6
        odd = 1.8
        ev = prob * odd - 1

        jogos.append({
            "jogo": f"{home} vs {away}",
            "aposta": "Vitoria Casa",
            "odd": odd,
            "ev": round(ev, 2)
        })

    return jogos": f"Time A vs Time B {i}",
                "aposta": "Vitoria Casa",
                "odd": odd,
                "ev": round(ev, 2)
            })

    return jogos
