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
    jogos = [
        {
            "jogo": "Flamengo vs Palmeiras",
            "prob": 0.65,
            "odd": 2.0,
            "ev": 0.30
        },
        {
            "jogo": "Real Madrid vs Barcelona",
            "prob": 0.60,
            "odd": 1.9,
            "ev": 0.14
        },
        {
            "jogo": "Manchester City vs Arsenal",
            "prob": 0.62,
            "odd": 2.1,
            "ev": 0.30
        }
    ]

    return jogos
    except Exception as e:
        return {"erro": str(e)}
