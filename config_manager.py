import json
CONFIG_PATH = "goat_config.json"

def load_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_config(data):
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=2)
