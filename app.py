import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from data.fetcher import get_market_data
from quantum.qubo import build_portfolio_qubo
from quantum.solver import solve_quantum_portfolio

# --- Page Configuration ---
st.set_page_config(
    page_title="Quantum Portfolio Optimizer",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Quantum Financial Portfolio Optimizer")
st.markdown("""
This application solves the **Markowitz Portfolio Optimization Problem** using quantum algorithms. 
It converts financial return/covariance matrices into a **Quadratic Unconstrained Binary Optimization (QUBO)** problem and solves it using **QAOA** on a simulated quantum backend.
""")

st.sidebar.header("Configuration Settings")

# --- User Inputs ---
default_tickers = "AAPL, MSFT, GOOGL, AMZN, NVDA"
ticker_input = st.sidebar.text_input("Stock Tickers (comma-separated):", default_tickers)
tickers = [t.strip().upper() for t in ticker_input.split(",") if t.strip()]

start_date = st.sidebar.date_input("Start Date", value=None)
# Fallback to default date string if not modified
start_str = start_date.strftime("%Y-%m-%d") if start_date else "2023-01-01"

budget = st.sidebar.slider(
    "Asset Budget (Number of assets to pick):",
    min_value=1,
    max_value=max(len(tickers), 1),
    value=min(3, len(tickers))
)

risk_factor = st.sidebar.slider(
    "Risk Aversion Factor (0 = Max Return, 1 = Min Risk):",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.05
)

# --- Execution Section ---
if st.sidebar.button("Run Quantum Optimization", type="primary"):
    if len(tickers) < 2:
        st.error("Please enter at least two stock tickers.")
    else:
        with st.spinner("Fetching market data and running QAOA circuit on simulator..."):
            try:
                # Step 1: Fetch Data
                mu, sigma, names = get_market_data(tickers, start_date=start_str)

                # Step 2: Formulate QUBO
                qubo, qp = build_portfolio_qubo(mu, sigma, risk_factor=risk_factor, budget=budget)

                # Step 3: Quantum Solver
                result = solve_quantum_portfolio(qubo)

                # Step 4: Extract Results
                selected_indices = [i for i, val in enumerate(result.x) if val == 1]
                selected_assets = [names[i] for i in selected_indices]

                # --- Metrics Dashboard ---
                col1, col2, col3 = st.columns(3)
                col1.metric("Optimal Objective Value", f"{result.fval:.4f}")
                col2.metric("Assets Selected", f"{len(selected_assets)} / {budget}")
                col3.metric("Quantum Engine", "Qiskit Aer QAOA")

                st.subheader("Recommended Portfolio")
                st.success(f"**Selected Assets:** {', '.join(selected_assets)}")

                # --- Visualizations ---
                col_left, col_right = st.columns(2)

                with col_left:
                    st.markdown("#### Selected Assets")
                    fig, ax = plt.subplots(figsize=(6, 4))
                    colors = ['#2ecc71' if i in selected_indices else '#e74c3c' for i in range(len(names))]
                    ax.bar(names, result.x, color=colors)
                    ax.set_ylabel("Selection (1 = Selected, 0 = Excluded)")
                    ax.set_title("Quantum Optimization Selection")
                    st.pyplot(fig)

                with col_right:
                    st.markdown("#### Covariance Matrix Heatmap")
                    fig_cov, ax_cov = plt.subplots(figsize=(6, 4))
                    sns.heatmap(sigma, annot=True, xticklabels=names, yticklabels=names, cmap="Blues", ax=ax_cov)
                    ax_cov.set_title("Annualized Asset Covariance")
                    st.pyplot(fig_cov)

            except Exception as e:
                st.error(f"Error during quantum execution: {str(e)}")

# --- Footer Info ---
st.markdown("---")
st.caption("Powered by **Qiskit 1.0+**, **Qiskit Optimization**, and **Streamlit**.")