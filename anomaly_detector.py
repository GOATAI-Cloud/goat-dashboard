# anomaly_detector.py

def detect_anomalies(sentiment_history, threshold=0.5):
    alerts = []
    for symbol, data in sentiment_history.items():
        pos = data.get("pos", 0)
        neg = data.get("neg", 0)
        if abs(pos - neg) < threshold:
            alerts.append(f"⚠️ Sentiment anomaly on {symbol}: balanced sentiment detected (pos={pos}, neg={neg})")
    return alerts

