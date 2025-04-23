import os
import json
import pytz
import talib
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from transformers import pipeline
from alpaca_trade_api.rest import REST
from lumibot.brokers import Alpaca
from lumibot.strategies.strategy import Strategy

# === GOAT Bot Modules ===
from quantum_utils import generate_quantum_randomness, monte_carlo_price_simulation, apply_entanglement_logic
from behavioral_ai import analyze_behavioral_patterns
from anomaly_detector import detect_anomalies
from auto_optimizer import optimize_thresholds
from trade_explainer import explain_trade
from ai_strategy_switcher import switch_strategy
from risk_profile_adapter import adapt_risk_profile
from cooldown_optimizer import optimize_cooldown
from config_manager import load_config, save_config
from price_utils import get_price  # new fallback price logic

# === Alpaca Config ===
ALPACA_CREDS = {
    "key_id": "AKLEJ09WRN086KZ50D7Y",
    "secret_key": "6ZIK0GCtiVV323M4lb44fjNqYNN9kohsVad0ZuEH",
    "base_url": "https://api.alpaca.markets"
}
LUMIBOT_CREDS = {
    "API_KEY": ALPACA_CREDS["key_id"],
    "API_SECRET": ALPACA_CREDS["secret_key"],
    "BASE_URL": ALPACA_CREDS["base_url"],
    "PAPER": False
}

# === Globals ===
sentiment_analyzer = pipeline("sentiment-analysis")
MEMORY_FILE = "goat_memory.json"
TICKERS = [
    "GURE", "HPH", "RTC", "GRAB", "MSGM", "BOWN", "CAPR", "EXEL", "RKT", "MMM", "MP", "PLTR",
    "AMAT", "SOLV", "TEM", "CP", "F", "NU", "PLD", "BSX", "NUE", "BITO", "BTC", "DOGE", "GLD",
    "ARM", "DGNX", "MSFT", "QQQ", "SPY", "VOO", "NVDA", "KGC", "WMT", "UAL", "LDOS", "PEGA",
    "TSLA", "RGTI", "INOD", "WTW", "SPG"
]
BUY_THRESHOLD = 0.85
SELL_THRESHOLD = 0.85
STOP_LOSS_PERCENTAGE = 0.05
COOLDOWN_MINUTES = 5

class GOATBot(Strategy):
    def initialize(self):
        self.sleeptime = "1M"
        self.api = REST(**ALPACA_CREDS)
        self.last_trade_times = {}
        self.price_memory = {}
        self.sentiment_history = {}
        self.learned_sentiment = self._load_memory()

    def on_trading_iteration(self):
        global BUY_THRESHOLD, SELL_THRESHOLD, STOP_LOSS_PERCENTAGE

        if os.path.exists("dashboard_config.json"):
            config = load_config()
            BUY_THRESHOLD = config.get("BUY_THRESHOLD", BUY_THRESHOLD)
            SELL_THRESHOLD = config.get("SELL_THRESHOLD", SELL_THRESHOLD)
            STOP_LOSS_PERCENTAGE = config.get("STOP_LOSS_PERCENTAGE", STOP_LOSS_PERCENTAGE)

        try:
            account = self.api.get_account()
            with open("alpaca_account.json", "w") as f:
                json.dump({
                    "cash": float(account.cash),
                    "equity": float(account.equity),
                    "buying_power": float(account.buying_power),
                    "portfolio_value": float(account.portfolio_value)
                }, f, indent=2)
        except Exception as e:
            print(f"[ERROR] Account sync failed: {e}")

        try:
            positions = self.api.list_positions()
            pos_data = []
            for p in positions:
                pos_data.append({
                    "Symbol": p.symbol,
                    "Qty": float(p.qty),
                    "Avg Price": float(p.avg_entry_price),
                    "Current Price": float(p.current_price),
                    "Unrealized PnL": float(p.unrealized_pl),
                    "PnL %": float(p.unrealized_plpc) * 100
                })
            pd.DataFrame(pos_data).to_csv("open_positions.csv", index=False)
        except Exception as e:
            print(f"[ERROR] Position sync failed: {e}")

        thresholds = optimize_thresholds(self.learned_sentiment)
        BUY_THRESHOLD, SELL_THRESHOLD = thresholds["buy"], thresholds["sell"]

        entangled_sentiments = {}
        for symbol in TICKERS:
            if self._in_cooldown(symbol):
                continue
            try:
                news_items = self.api.get_news(symbol, limit=5)
                headlines = [item.headline for item in news_items if hasattr(item, 'headline')]
                sentiment = sentiment_analyzer(headlines)
                pos_max = max((s['score'] for s in sentiment if s['label'] == "POSITIVE"), default=0)
                neg_max = max((s['score'] for s in sentiment if s['label'] == "NEGATIVE"), default=0)
            except:
                pos_max, neg_max = 0, 0

            last = self.sentiment_history.get(symbol, {"pos": 0, "neg": 0})
            self.sentiment_history[symbol] = {"pos": pos_max, "neg": neg_max}
            self._update_learning(symbol, pos_max, neg_max)
            entangled_sentiments[symbol] = (pos_max, neg_max)

        entangled_sentiments = apply_entanglement_logic(entangled_sentiments)
        anomaly_flags = detect_anomalies(self.sentiment_history)

        for symbol, (pos_max, neg_max) in entangled_sentiments.items():
            if anomaly_flags.get(symbol):
                continue
            try:
                historical = self.api.get_bars(symbol, "1D", limit=50).df
                if len(historical) < 30:
                    continue
                close = historical["close"].values
                rsi = talib.RSI(close)[-1]
                adx = talib.ADX(historical["high"], historical["low"], close)[-1]
                signal = switch_strategy(pos_max, neg_max, pos_max - last["pos"], neg_max - last["neg"], BUY_THRESHOLD, SELL_THRESHOLD, rsi)
                reason = explain_trade(symbol, pos_max, neg_max, signal)
                print(f"[EXPLAIN] {symbol}: {reason} | RSI={rsi:.2f} | ADX={adx:.2f}")

                if signal == "positive":
                    self._buy(symbol, pos_max)
                elif signal == "negative":
                    self._sell(symbol, neg_max)
                self._check_stop_loss(symbol)
            except Exception as e:
                print(f"[ERROR] Failed for {symbol}: {e}")

    def _buy(self, symbol, score):
        if self.get_position(symbol): return
        cash = self.get_cash()
        price = get_price(symbol, self.api)
        if not price or cash < price: return
        forecast, _ = monte_carlo_price_simulation(price)
        if forecast < price: return
        qty = int(((cash / len(TICKERS)) * generate_quantum_randomness()) / price)
        if qty > 0:
            self.price_memory[symbol] = price
            self.submit_order(self.create_order(symbol, qty, "buy"))
            self.last_trade_times[symbol] = datetime.now()
            self._log_trade("BUY", symbol, qty, price, score)
            print(f"[BUY CHECK] Symbol: {symbol} | Price: {price} | Qty: {qty}")


    def _sell(self, symbol, score):
        pos = self.get_position(symbol)
        if pos:
            qty = int(pos.quantity)
            price = get_price(symbol, self.api)
            self.submit_order(self.create_order(symbol, qty, "sell"))
            self.last_trade_times[symbol] = datetime.now()
            self._log_trade("SELL", symbol, qty, price, score)

    def _check_stop_loss(self, symbol):
        pos = self.get_position(symbol)
        if not pos or symbol not in self.price_memory: return
        price = get_price(symbol, self.api)
        entry = self.price_memory[symbol]
        if price and price < entry * (1 - STOP_LOSS_PERCENTAGE):
            qty = int(pos.quantity)
            self.submit_order(self.create_order(symbol, qty, "sell"))
            del self.price_memory[symbol]
            self.last_trade_times[symbol] = datetime.now()
            self._log_trade("STOP-LOSS", symbol, qty, price, -1)

    def _in_cooldown(self, symbol):
        last = self.last_trade_times.get(symbol)
        return last and (datetime.now() - last < timedelta(minutes=optimize_cooldown(COOLDOWN_MINUTES)))

    def _log_trade(self, action, symbol, qty, price, score):
        time = datetime.now(pytz.timezone("America/New_York")).strftime("%Y-%m-%d %H:%M:%S")
        with open("goatbot_trades.log", "a") as f:
            f.write(f"{time}: {action} {qty} {symbol} at ${price:.2f} (score: {score:.3f})\n")
        print(f"[LOGGED] {action} {qty} {symbol} at ${price:.2f} | score={score:.3f}")

    def _load_memory(self):
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE) as f:
                    return json.load(f)
            except: pass
        return {}

    def _update_learning(self, symbol, pos, neg):
        if symbol not in self.learned_sentiment:
            self.learned_sentiment[symbol] = []
        self.learned_sentiment[symbol].append({
            "timestamp": datetime.now().isoformat(),
            "pos": pos,
            "neg": neg
        })
        self.learned_sentiment[symbol] = self.learned_sentiment[symbol][-100:]
        with open(MEMORY_FILE, "w") as f:
            json.dump(self.learned_sentiment, f, indent=2)

    def on_bot_crash(self, exception):
        print(f"[CRITICAL] GOATBot crashed: {exception}")

# === Launch
if __name__ == "__main__":
    broker = Alpaca(LUMIBOT_CREDS)
    strategy = GOATBot(name="GOAT_Bot_5_0", broker=broker)
    strategy.run_live()
