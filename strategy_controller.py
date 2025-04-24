# strategy_controller.py
import json
import os

STATUS_FILE = "logs/warp_status.json"

DEFAULT_CONFIG = {
    "quantum": True,
    "anomaly": True,
    "auto_strategy": True
}

def get_warp_status():
    if not os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "w") as f:
            json.dump(DEFAULT_CONFIG, f)
    with open(STATUS_FILE, "r") as f:
        return json.load(f)

def toggle_strategy_mode(quantum, anomaly, auto_strategy):
    new_config = {
        "quantum": quantum,
        "anomaly": anomaly,
        "auto_strategy": auto_strategy
    }
    with open(STATUS_FILE, "w") as f:
        json.dump(new_config, f)
