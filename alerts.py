# alerts.py
import random

def check_alerts():
    pool = [
        "🔔 Trade volume spike in AAPL",
        "⚠️ Sentiment reversal on TSLA",
        "🧠 Strategy switch triggered for SPY",
        "📡 Social media burst around NVDA"
    ]
    return random.sample(pool, k=2)
