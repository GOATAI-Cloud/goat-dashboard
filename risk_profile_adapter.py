# risk_profile_adapter.py

def adjust_risk(data, risk_level="moderate"):
    """
    Used by GOAT Bot Cloud.
    Adjusts trade quantity based on volatility and risk preference.
    """
    volatility = data['close'].pct_change().std()
    base_qty = 10

    if risk_level == "aggressive":
        return int(base_qty * (1 + volatility * 10))
    elif risk_level == "conservative":
        return int(base_qty * (1 - volatility * 5))
    else:
        return base_qty


def adapt_risk_profile(equity, pnl):
    """
    Used by GOAT Bot 6.0.
    Returns a string indicating the user's risk profile based on performance.
    """
    if pnl < -0.1 * equity:
        return "conservative"
    elif pnl > 0.1 * equity:
        return "aggressive"
    return "moderate"
