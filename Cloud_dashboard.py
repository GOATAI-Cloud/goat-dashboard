"""
GOAT Dashboard 1.0 🐐📊
Modular Streamlit UI for viewing sentiment, trade logs, and bot analytics.
"""

import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="GOAT Dashboard", layout="wide")
st.title("📊 GOAT Bot Cloud Dashboard")

# === Tabs ===
tabs = st.tabs(["📈 Trade Log", "💬 Commentary", "📊 Sentiment Scores", "⚙️ Settings"])

# === Trade Log Tab ===
with tabs[0]:
    st.header("📈 Daily Trade Log")
    log_path = "logs/daily_trade_log.csv"
    if os.path.exists(log_path):
        df = pd.read_csv(log_path)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No trades have been logged yet.")

# === Commentary Tab ===
with tabs[1]:
    st.header("💬 Trade Commentary")
    commentary_path = "goat_trade_commentary.json"
    if os.path.exists(commentary_path):
        commentary = pd.read_json(commentary_path)
        st.dataframe(commentary, use_container_width=True)
    else:
        st.info("Commentary will appear here once trades are made.")

# === Sentiment Scores Tab ===
with tabs[2]:
    st.header("📊 Entangled Sentiment Scores")
    sentiment_path = "logs/entangled_sentiments.csv"
    if os.path.exists(sentiment_path):
        df = pd.read_csv(sentiment_path)
        st.dataframe(df.sort_values("positive_score", ascending=False), use_container_width=True)
    else:
        st.info("Sentiment scores will populate once trading begins.")

# === Settings Placeholder ===
with tabs[3]:
    st.header("⚙️ Coming Soon: Bot Configuration Panel")
    st.markdown("This panel will allow live tuning of strategy, risk, cooldown, and filters.")
    st.button("🔄 Refresh Dashboard")