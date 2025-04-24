import json
import os

# === Shared config for GOAT Bot 6.0 ===
CONFIG_PATH = "goat_config.json"

def load_config():
    """
    Loads the shared GOAT 6.0 config file.
    """
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_config(data):
    """
    Saves the shared GOAT 6.0 config file.
    """
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=2)

# === Multi-user config for GOAT Bot Cloud ===
USER_CONFIG_DIR = "user_configs"

def load_user_config(username):
    """
    Loads per-user config from user_configs/{username}.json
    """
    os.makedirs(USER_CONFIG_DIR, exist_ok=True)
    config_file = os.path.join(USER_CONFIG_DIR, f"{username}.json")
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            return json.load(f)
    else:
        print(f"No config found for {username}. Using default settings.")
        return {
            "tickers": ["AAPL", "TSLA"],
            "risk_level": "moderate",
            "cooldown": 300
        }
