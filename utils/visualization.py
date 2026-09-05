import matplotlib.pyplot as plt
import seaborn as sns


def plot_portfolio_results(names, selected_indices):
    plt.figure(figsize=(8, 4))
    colors = ['#2ecc71' if i in selected_indices else '#bdc3c7' for i in range(len(names))]

    sns.barplot(x=names, y=[1 if i in selected_indices else 0 for i in range(len(names))], palette=colors)
    plt.title("Quantum Optimization - Selected Portfolio Assets")
    plt.ylabel("Selected (1 / 0)")
    plt.xlabel("Stock Ticker")
    plt.tight_layout()
    plt.savefig("portfolio_result.png")
    plt.show()