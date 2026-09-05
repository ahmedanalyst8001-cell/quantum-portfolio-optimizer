from data.fetcher import get_market_data
from quantum.qubo import build_portfolio_qubo
from quantum.solver import solve_quantum_portfolio
from utils.visualization import plot_portfolio_results


def run():
    print("=== Step 1: Fetching Market Data ===")
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"]
    mu, sigma, names = get_market_data(tickers)
    print(f"Assets loaded: {names}")

    print("\n=== Step 2: Formulating Quantum QUBO ===")
    qubo, qp = build_portfolio_qubo(mu, sigma, risk_factor=0.5, budget=3)

    print("\n=== Step 3: Running Quantum Optimization (QAOA) ===")
    result = solve_quantum_portfolio(qubo)

    print("\n=== Step 4: Quantum Optimization Results ===")
    selected_indices = [i for i, val in enumerate(result.x) if val == 1]
    selected_assets = [names[i] for i in selected_indices]

    print(f"Optimal Allocation Vector (x): {result.x}")
    print(f"Recommended Portfolio Assets: {selected_assets}")
    print(f"Optimal Objective Value: {result.fval:.4f}")

    plot_portfolio_results(names, selected_indices)


if __name__ == "__main__":
    run()