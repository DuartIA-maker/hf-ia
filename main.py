from fastapi import FastAPI
import random

app = FastAPI()

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
                "aposta": "Vitória Casa",
                "odd": odd,
                "ev": round(ev, 2)
            })

    return jogos
