def adapt_risk_profile(equity, pnl):
    if pnl < -0.1 * equity:
        return "conservative"
    elif pnl > 0.1 * equity:
        return "aggressive"
    return "moderate"
