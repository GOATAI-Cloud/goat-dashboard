# ai_strategy_switcher.py

def select_strategy(data):
    """
    Used by goat_bot_cloud.py – returns a strategy function.
    """
    def simple_ma_strategy(df):
        short_ma = df['close'].rolling(window=5).mean()
        long_ma = df['close'].rolling(window=20).mean()

        if short_ma.iloc[-1] > long_ma.iloc[-1] and short_ma.iloc[-2] <= long_ma.iloc[-2]:
            return "buy"
        elif short_ma.iloc[-1] < long_ma.iloc[-1] and short_ma.iloc[-2] >= long_ma.iloc[-2]:
            return "sell"
        else:
            return "hold"
    return simple_ma_strategy


def switch_strategy(data, config=None):
    """
    Used by goat_bot_6.0.py – returns a string signal directly.
    """
    short_ma = data['close'].rolling(window=5).mean()
    long_ma = data['close'].rolling(window=20).mean()

    if short_ma.iloc[-1] > long_ma.iloc[-1] and short_ma.iloc[-2] <= long_ma.iloc[-2]:
        return "buy"
    elif short_ma.iloc[-1] < long_ma.iloc[-1] and short_ma.iloc[-2] >= long_ma.iloc[-2]:
        return "sell"
    else:
        return "hold"
