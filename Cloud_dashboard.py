"""
GOAT BOT X – Level 1000 Interface 🐐⚛️👁️‍🗨️
Immersive trading dashboard with AI Oracle, Strategy Warp Panel, Tradesphere, and Godmode Console.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
from datetime import datetime
from strategy_controller import get_warp_status, toggle_strategy_mode
from oracle_engine import generate_trade_prediction
from tradesphere import generate_tradesphere_plot
from goat_console import execute_command
from anomaly_detector import detect_anomalies
from goat_voice import speak_summary
from alerts import check_alerts

st.set_page_config(page_title="GOAT BOT X Console", layout="wide")
st.title("🐐 GOAT BOT X – Command Interface")

# === Warp Status Toggle Panel ===
st.sidebar.header("⚙️ Strategy Warp Panel")
warp_config = get_warp_status()

with st.sidebar.form("warp_form"):
    quantum_enabled = st.checkbox("Enable Quantum Logic", value=warp_config.get("quantum", True))
    anomaly_detection = st.checkbox("Activate Anomaly Detector", value=warp_config.get("anomaly", True))
    auto_strategy = st.checkbox("Auto Strategy Mode", value=warp_config.get("auto_strategy", True))
    submitted = st.form_submit_button("Apply Warp Settings")
    if submitted:
        toggle_strategy_mode(quantum_enabled, anomaly_detection, auto_strategy)
        st.success("Warp settings updated.")

# === TABS ===
tabs = st.tabs(["🧠 Oracle", "🌐 Tradesphere", "⏱️ Anomaly Watch", "🗣️ Voice Summary", "🧬 Alerts", "⌨️ Godmode Console"])

# === Oracle Tab ===
with tabs[0]:
    st.subheader("AI Oracle – Trade Insights")
    prediction = generate_trade_prediction()
    st.markdown(f"**Prediction:** {prediction['text']}")
    st.metric("Confidence", f"{prediction['confidence']}%")
    with open("logs/ai_oracle_log.json", "w") as f:
        json.dump(prediction, f, indent=2)

# === Tradesphere Tab ===
with tabs[1]:
    st.subheader("🌐 Tradesphere Visualization")
    fig = generate_tradesphere_plot()
    st.plotly_chart(fig, use_container_width=True)

# === Anomaly Watch Tab ===
with tabs[2]:
    st.subheader("⏱️ Real-time Sentiment Anomalies")
    try:
        with open("logs/sentiment_history.json") as f:
            sentiment_data = json.load(f)
        anomalies = detect_anomalies(sentiment_data)
    except Exception as e:
        anomalies = [f"Error loading sentiment data: {str(e)}"]

    if anomalies:
        st.warning("Anomalies detected!")
        for alert in anomalies:
            st.write(alert)
        with open("logs/anomalies.json", "w") as f:
            json.dump(anomalies, f, indent=2)
    else:
        st.success("No anomalies found in current cycle.")

# === Voice Summary Tab ===
with tabs[3]:
    st.subheader("🗣️ Daily Trade Summary – Audio")
    summary = speak_summary()
    st.text(summary)
    with open("logs/voice_summary.txt", "w") as f:
        f.write(summary)

# === Alerts Tab ===
with tabs[4]:
    st.subheader("🧬 Omni-Alert Feed")
    alerts = check_alerts()
    for alert in alerts:
        st.info(alert)

# === Godmode Console ===
with tabs[5]:
    st.subheader("⌨️ Execute Divine Commands")
    user_cmd = st.text_input("Console Command")
    if user_cmd:
        output = execute_command(user_cmd)
        st.code(output)
