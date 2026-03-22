from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

# LIBERAR ACESSO DO SITE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "HF Odds Engine Online 🔥"}

@app.get("/value-bets")
def value_bets():
    jogos = []

    for i in range(5):
        prob = random.uniform(0.55, 0.7)
        odd = 1.8
        ev = prob * odd - 1

        if ev > 0:
            jogos.append({
                "jogo": f"Time A vs Time B {i}",
                "aposta": "Vitoria Casa",
                "odd": odd,
                "ev": round(ev, 2)
            })

    return jogos
