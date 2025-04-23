# cooldown_optimizer.py

import os
import json
from datetime import datetime, timedelta

COOLDOWN_PATH = "logs/cooldown_tracker.json"

def load_cooldowns():
    if not os.path.exists(COOLDOWN_PATH):
        return {}
    with open(COOLDOWN_PATH, "r") as f:
        return json.load(f)

def save_cooldowns(data):
    with open(COOLDOWN_PATH, "w") as f:
        json.dump(data, f, indent=4)

def should_trade_now(username, ticker, cooldown_seconds=300):
    """
    Used by GOAT Bot Cloud – checks if a cooldown has passed for this user/ticker.
    """
    cooldowns = load_cooldowns()
    key = f"{username}_{ticker}"
    now = datetime.utcnow()

    last_trade = cooldowns.get(key)
    if last_trade:
        last_trade_time = datetime.fromisoformat(last_trade)
        if now < last_trade_time + timedelta(seconds=cooldown_seconds):
            return False

    cooldowns[key] = now.isoformat()
    save_cooldowns(cooldowns)
    return True

def optimize_cooldown(trade_history, base_cooldown=300):
    """
    Used by GOAT Bot 6.0 – adjusts cooldown time based on trade history stats.
    """
    # Dummy logic for now; can be upgraded later
    win_rate = trade_history.get('win_rate', 0.5)
    
    if win_rate > 0.6:
        return int(base_cooldown * 0.8)  # More aggressive
    elif win_rate < 0.4:
        return int(base_cooldown * 1.2)  # More conservative
    else:
        return base_cooldown
