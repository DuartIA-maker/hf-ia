from fastapi import FastAPI
import random

app = FastAPI()

@app.get("/value-bets")
def value():
    jogos = []
    for i in range(5):
        prob = random.uniform(0.55,0.7)
        odd = 1.8
        ev = prob*odd -1

        if ev > 0:
            jogos.append({
                "jogo": f"TimeA vs TimeB {i}",
                "aposta": "Vitória Casa",
                "odd": odd,
                "ev": round(ev,2)
            })
    return jogos
