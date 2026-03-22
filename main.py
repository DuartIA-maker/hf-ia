from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests, math, json, os

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

MODEL_FILE = "model.json"

# -------------------------
# MODELO APRENDIZADO
# -------------------------
def load_model():
    if not os.path.exists(MODEL_FILE):
        return {"bias": 1.0}
    with open(MODEL_FILE) as f:
        return json.load(f)

def save_model(model):
    with open(MODEL_FILE, "w") as f:
        json.dump(model, f)

model = load_model()

# -------------------------
# POISSON
# -------------------------
def poisson(k, lamb):
    return (lamb**k * math.exp(-lamb)) / math.factorial(k)

# -------------------------
# ESTATÍSTICAS
# -------------------------
def get_team_stats(team_id):
    url = f"https://api.football-data.org/v4/teams/{team_id}/matches?limit=10"
    headers = {"X-Auth-Token": FOOTBALL_API_KEY}
    data = requests.get(url, headers=headers).json()

    gols_m, gols_s, jogos = 0, 0, 0

    for m in data.get("matches", []):
        if m["score"]["fullTime"]["home"] is None:
            continue

        if m["homeTeam"]["id"] == team_id:
            gm = m["score"]["fullTime"]["home"]
            gs = m["score"]["fullTime"]["away"]
        else:
            gm = m["score"]["fullTime"]["away"]
            gs = m["score"]["fullTime"]["home"]

        gols_m += gm
        gols_s += gs
        jogos += 1

    if jogos == 0:
        return 1.2, 1.2

    return gols_m / jogos, gols_s / jogos

# -------------------------
# ODDS
# -------------------------
def get_odds():
    url = f"https://api.the-odds-api.com/v4/sports/soccer/odds/?apiKey={ODDS_API_KEY}&regions=eu&markets=h2h"
    return requests.get(url).json()

# -------------------------
# GERAR APOSTAS
# -------------------------
@app.get("/value-bets")
def value_bets():

    matches = requests.get(
        "https://api.football-data.org/v4/matches",
        headers={"X-Auth-Token": FOOTBALL_API_KEY}
    ).json()

    odds_data = get_odds()

    jogos = []

    for m in matches.get("matches", [])[:5]:

        home = m["homeTeam"]
        away = m["awayTeam"]

        g_home, s_home = get_team_stats(home["id"])
        g_away, s_away = get_team_stats(away["id"])

        league_avg = 1.35

        lambda_home = (g_home / league_avg) * (s_away / league_avg) * league_avg * 1.1
        lambda_away = (g_away / league_avg) * (s_home / league_avg) * league_avg

        prob_home = 0

        for i in range(6):
            for j in range(6):
                p = poisson(i, lambda_home) * poisson(j, lambda_away)
                if i > j:
                    prob_home += p

        # 🔥 IA ajustando probabilidade
        prob_home *= model["bias"]

        # Odds
        odd = None
        for game in odds_data:
            try:
                if home["name"].lower() in game["home_team"].lower():
                    odd = game["bookmakers"][0]["markets"][0]["outcomes"][0]["price"]
                    break
            except:
                continue

        if odd:
            ev = prob_home * odd - 1

            if ev > 0.05:
                jogos.append({
                    "jogo": f"{home['name']} vs {away['name']}",
                    "prob": round(prob_home, 2),
                    "odd": odd,
                    "ev": round(ev, 2)
                })

    return jogos

# -------------------------
# SALVAR RESULTADO (APRENDER)
# -------------------------
@app.post("/resultado")
def resultado(acertou: bool):
    global model

    if acertou:
        model["bias"] *= 1.02
    else:
        model["bias"] *= 0.98

    save_model(model)

    return {"novo_modelo": model}
