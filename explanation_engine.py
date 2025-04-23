# explanation_engine.py

import random

def explain_trade(ticker, signal, strategy_name, risk_level):
    """
    Generates a GPT-style explanation for a trade decision with emoji flair.
    """

    base_explanations = {
        "buy": [
            f"{ticker} showed bullish momentum 📈 based on the {strategy_name} strategy. Risk level '{risk_level}' aligns with a strong entry point. Let’s ride this wave 🌊.",
            f"AI detected a breakout on {ticker} 🔓 via {strategy_name}. Current risk mode: '{risk_level}'. Momentum and sentiment are aligned — executing BUY 💸.",
            f"{strategy_name} gave us the green light 🚦. Market data and quantum vibes are bullish — buying {ticker} under '{risk_level}' risk conditions."
        ],
        "sell": [
            f"{ticker} is showing reversal signals 🧨 under the {strategy_name} model. Risk profile '{risk_level}' suggests locking in gains. SELL triggered 💼.",
            f"Sentiment + techs suggest {ticker} has peaked 📉. Strategy {strategy_name} confirms. Risk setting '{risk_level}' supports this exit call. Selling ✅.",
            f"Indicators are cooling off for {ticker} 🥶. {strategy_name} recommends trimming exposure. Executing SELL under risk mode: '{risk_level}'."
        ],
        "hold": [
            f"{strategy_name} reports neutral conditions ⚖️ on {ticker}. Risk level '{risk_level}' advises to HOLD and wait for confirmation 🕰️.",
            f"No strong move detected for {ticker}. Strategy {strategy_name} and current market alignment under '{risk_level}' risk says: HOLD 🛑.",
            f"Staying patient 🧘 — {ticker} doesn't justify action right now. {strategy_name} and risk level '{risk_level}' align on HOLD."
        ]
    }

    explanation = random.choice(base_explanations.get(signal, [f"No valid signal for {ticker} via {strategy_name}."]))
    return explanation
