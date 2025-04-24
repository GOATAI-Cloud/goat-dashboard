# tradesphere.py
import plotly.express as px
import pandas as pd
from datetime import datetime

def generate_tradesphere_plot():
    # Fake market energy data
    data = {
        "ticker": ["TSLA", "AAPL", "SPY", "NVDA", "META"],
        "sentiment": [0.7, 0.6, 0.55, 0.8, 0.4],
        "volatility": [0.3, 0.25, 0.2, 0.35, 0.28],
        "impact": [0.9, 0.7, 0.6, 0.85, 0.5]
    }
    df = pd.DataFrame(data)
    fig = px.scatter_3d(
        df, x="sentiment", y="volatility", z="impact",
        color="ticker", size="impact",
        title="Tradesphere – AI Market Pulse"
    )
    return fig