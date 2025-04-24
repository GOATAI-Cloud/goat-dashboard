"""
GOAT Bot Cloud - Multi-user AI Trading Engine 🌩️🐐
Supports session-based Alpaca credentials, config loading, trade triggering, and AI logic.
Plug-and-play into Streamlit or Flask for frontend user controls.
"""

import time
import json
import traceback
import logging
import pandas as pd
from datetime import datetime
import os
import streamlit as st

from ai_strategy_switcher import select_strategy
from cooldown_optimizer import should_trade_now
from risk_profile_adapter import adjust_risk
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from explanation_engine import explain_trade
from quantum_utils import quantum_random, apply_entanglement
from config_manager import load_user_config
from alpaca_trade_api.rest import REST, TimeFrame

# === Load API keys for Finnhub and Twelve Data ===
with open("data_keys.json") as f:
    data_keys = json.load(f)
    FINNHUB_KEY = data_keys.get("finnhub_key")
    TWELVE_KEY = data_keys.get("twelve_data_key")

# === Ensure logs/ directory exists ===
os.makedirs("logs", exist_ok=True)

# === Setup Logging ===
logging.basicConfig(filename="logs/cloud_errors.log", level=logging.ERROR)

# === Load User Sessions ===
with open("user_sessions.json") as f:
    user_sessions = json.load(f)

# === Main Trading Loop Per User ===
def run_trade_cycle_for_user(username, creds, config):
    try:
        st.write(f"[GOAT] Starting trade cycle for user: {username}")
        api = REST(creds['key'], creds['secret'], creds['base_url'])

        tickers = config.get("tickers", ["AAPL", "TSLA"])
        risk_level = config.get("risk_level", "medium")
        cooldown = config.get("cooldown", 300)

        for ticker in tickers:
            if not should_trade_now(username, ticker, cooldown):
                st.write(f"[Cooldown] Skipping {ticker} for {username}")
                continue

            data = api.get_bars(ticker, TimeFrame.Minute, limit=50).df
            if data.empty:
                st.write(f"[Data] No data for {ticker}")
                continue

            strategy = select_strategy(data)
            risk_adj = adjust_risk(data, risk_level)
            signal = strategy(data)

            # Quantum Entanglement Logic
            signal = apply_entanglement(signal)
            rand_factor = quantum_random()

            if signal == "buy" and rand_factor > 0.5:
                qty = int(risk_adj)
                api.submit_order(symbol=ticker, qty=qty, side="buy", type="market", time_in_force="gtc")
                st.success(f"[TRADE] {username} bought {qty} shares of {ticker}")

                reason = explain_trade(ticker, signal, strategy.__name__, risk_level)
                st.write(f"[EXPLAIN] {reason}")

                # === Log Trade Explanation to CSV ===
                log_entry = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "user": username,
                    "ticker": ticker,
                    "action": signal,
                    "qty": qty,
                    "strategy": strategy.__name__,
                    "risk_level": risk_level,
                    "explanation": reason
                }

                log_path = "logs/daily_trade_log.csv"
                try:
                    df_log = pd.read_csv(log_path)
                    df_log = pd.concat([df_log, pd.DataFrame([log_entry])], ignore_index=True)
                except FileNotFoundError:
                    df_log = pd.DataFrame([log_entry])

                df_log.to_csv(log_path, index=False)

    except Exception as e:
         error_message = f"Error in trade cycle for {username}: {str(e)}"
         traceback_str = traceback.format_exc()

    # Display cleanly in Streamlit
    st.error(f"❌ {error_message}")
    with st.expander("See full traceback"):
        st.text(traceback_str)

    # Attempt to log to file
    try:
        logging.error(f"{error_message}\n{traceback_str}")
    except Exception as log_err:
        st.warning(f"Logging failed: {log_err}")

# === Streamlit-Compatible Execution ===
st.set_page_config(page_title="GOAT Bot Cloud", layout="centered")
st.title("🐐 GOAT Bot Cloud — One Cycle Test")

for user, session in user_sessions.items():
    config = load_user_config(user)
    run_trade_cycle_for_user(user, session['creds'], config)

st.success("✅ All user trade cycles complete.")