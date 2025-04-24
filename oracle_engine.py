# oracle_engine.py
import random

def generate_trade_prediction():
    options = [
        {"text": "Buy TSLA within next 15 mins.", "confidence": 91},
        {"text": "Hold AAPL, momentum cooling.", "confidence": 77},
        {"text": "Watch NVDA for breakout above resistance.", "confidence": 85},
        {"text": "Avoid META today, sentiment divergence detected.", "confidence": 68}
    ]
    return random.choice(options)