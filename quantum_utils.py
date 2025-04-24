import numpy as np
import pandas as pd
import random

USE_QISKIT = False

try:
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator
    from qiskit.compiler import transpile
    USE_QISKIT = True
except ImportError:
    print("Qiskit not available — falling back to pseudo-random mode.")

def generate_quantum_randomness(num_bits=3, precision=3):
    if USE_QISKIT:
        qc = QuantumCircuit(num_bits, num_bits)
        for i in range(num_bits):
            qc.h(i)
            qc.measure(i, i)
        simulator = AerSimulator()
        compiled = transpile(qc, simulator)
        result = simulator.run(compiled, shots=1).result()
        bitstring = list(result.get_counts().keys())[0]
        return round(int(bitstring, 2) / (2**num_bits), precision)
    else:
        return round(random.random(), precision)

def monte_carlo_price_simulation(current_price, drift=0.001, volatility=0.02, days=5, simulations=100):
    results = []
    for _ in range(simulations):
        price = current_price
        for _ in range(days):
            price *= np.exp((drift - 0.5 * volatility**2) + volatility * np.random.normal())
        results.append(price)
    return np.mean(results), np.std(results)

def load_sentiment_scores(path="Sentiment_Scorecards.csv"):
    try:
        df = pd.read_csv(path)
        return {
            row["ticker"]: (row["positive_score"], row["negative_score"])
            for _, row in df.iterrows()
        }
    except Exception as e:
        print(f"Error loading sentiment scores: {e}")
        return {}

def apply_entanglement_logic(ticker_scores):
    if not ticker_scores:
        return {}

    avg_pos = sum(score[0] for score in ticker_scores.values()) / len(ticker_scores)
    avg_neg = sum(score[1] for score in ticker_scores.values()) / len(ticker_scores)

    entangled_scores = {
        symbol: (
            (pos + avg_pos) / 2,
            (neg + avg_neg) / 2
        ) for symbol, (pos, neg) in ticker_scores.items()
    }

    return entangled_scores

# Backward compatibility with GOAT Bot Cloud's previous call structure
quantum_random = generate_quantum_randomness
apply_entanglement = lambda signal: signal  # Placeholder to avoid errors in Cloud if not using full entanglement
