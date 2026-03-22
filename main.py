from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests, math

FOOTBALL_API_KEY = "810bc8056a3c4df2bcdb3ffa1e9383f9"
ODDS_API_KEY = "7bc3b2c93efa2cc07ba839ff0fd9710d"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# POISSON
def poisson(k, lamb):
    return (lamb**k * math.exp(-lamb)) / math.factorial(k)

# PEGAR ODDS UMA VEZ
def get_odds():
    url = f"https://api.the-odds-api.com/v4/sports/soccer/odds/?apiKey={ODDS_API_KEY}&regions=eu&markets=h2h"
    return requests.get(url).json()

@app.get("/")
def home():
    return {"status": "HF Odds Engine rodando 🔥"}

@app.get("/value-bets")
def value_bets():

    # 🔥 UMA CHAMADA
    matches = requests.get(
        "https://api.football-data.org/v4/matches",
        headers={"X-Auth-Token": FOOTBALL_API_KEY}
    ).json()

    # 🔥 UMA CHAMADA
    odds_data = get_odds()

    jogos = []

    for m in matches.get("matches", [])[:3]:  # 🔥 reduzir carga

        home_name = m["homeTeam"]["name"]
        away_name = m["awayTeam"]["name"]

        # ⚠️ VALORES FIXOS TEMPORÁRIOS (evita travamento)
        lambda_home = 1.5
        lambda_away = 1.2

        prob_home = 0

        for i in range(5):
            for j in range(5):
                p = poisson(i, lambda_home) * poisson(j, lambda_away)
                if i > j:
                    prob_home += p

        odd_real = None

        for game in odds_data:
            try:
                if home_name.lower() in game["home_team"].lower():
                    odd_real = game["bookmakers"][0]["markets"][0]["outcomes"][0]["price"]
                    break
            except:
                continue

        if odd_real:
            ev = prob_home * odd_real - 1

            if ev > 0:
                jogos.append({
                    "jogo": f"{home_name} vs {away_name}",
                    "prob": round(prob_home, 2),
                    "odd": odd_real,
                    "ev": round(ev, 2)
                })

    return jogos
