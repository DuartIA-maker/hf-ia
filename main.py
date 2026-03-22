from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests, math

FOOTBALL_API_KEY = "810bc8056a3c4df2bcdb3ffa1e9383f9"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def poisson(k, lamb):
    return (lamb**k * math.exp(-lamb)) / math.factorial(k)

@app.get("/")
def home():
    return {"status": "HF Odds Engine rodando 🔥"}

@app.get("/value-bets")
def value_bets():
    try:
        res = requests.get(
            "https://api.football-data.org/v4/matches",
            headers={"X-Auth-Token": FOOTBALL_API_KEY},
            timeout=5  # 🔥 evita travar
        )

        data = res.json()

        jogos = []

        for m in data.get("matches", [])[:3]:  # 🔥 só 3 jogos

            home = m["homeTeam"]["name"]
            away = m["awayTeam"]["name"]

            lambda_home = 1.5
            lambda_away = 1.2

            prob = 0

            for i in range(5):
                for j in range(5):
                    p = poisson(i, lambda_home) * poisson(j, lambda_away)
                    if i > j:
                        prob += p

            odd = 1.8
            ev = prob * odd - 1

            jogos.append({
                "jogo": f"{home} vs {away}",
                "prob": round(prob, 2),
                "odd": odd,
                "ev": round(ev, 2)
            })

        return jogos

    except Exception as e:
        return {"erro": str(e)}
