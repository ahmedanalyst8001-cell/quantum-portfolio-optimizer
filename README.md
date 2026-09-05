# Quantum Portfolio Optimizer

An end-to-end, enterprise-grade quantum-classical hybrid financial application designed to solve the **Markowitz Mean-Variance Portfolio Optimization Problem** using **Quantum Approximate Optimization Algorithms (QAOA)**. 

Built on top of **Qiskit 2.x**, **Qiskit Optimization**, and **Streamlit**, this engine formulates mathematical portfolio constraints into a **Quadratic Unconstrained Binary Optimization (QUBO)** problem, maps it to an Ising Hamiltonian, and solves for the optimal asset allocation vector on quantum hardware simulators and physical NISQ (Noisy Intermediate-Scale Quantum) backends.

---

## Key Features

- **Dynamic Market Data Ingestion:** Real-time ingestion of historical stock metrics via Yahoo Finance with automated risk-free rate adjustment, annualized expected returns ($\boldsymbol{\mu}$), and asset covariance ($\boldsymbol{\Sigma}$) calculation.
- **Ising / QUBO Formulation:** Automated conversion of modern portfolio theory (MPT) objective functions and budget constraints into QUBO matrices suited for variational quantum execution.
- **Qiskit 2.x Variational Circuit Pipeline:** State-of-the-art implementation using `QAOA`, `StatevectorSampler`, and `COBYLA` classical optimizers.
- **Interactive Web UI:** Interactive dashboard built with Streamlit for dynamic ticker selection, custom date ranges, risk-tolerance configuration, and quantum convergence visualization.
- **Resilient Execution Engine:** Built-in error handling for market data retrieval, SQLite cache lock suppression, and complex-coefficient runtime sanitization.

---

## Architectural Workflow
[ Financial Market Data ]│ (Yahoo Finance API)▼[ Mean-Variance Matrix Setup ] ──► Compute Expectation Vector (μ) & Covariance (Σ)│▼[ QUBO Hamiltonian Mapping ]  ──► Formulate Penalty Terms & Constraints│▼[ QAOA Variational Circuit ]  ──► StatevectorSampler & COBYLA Optimization│▼[ Optimal Bitstring Extraction ]──► Portfolio Vector & Allocation Visualization
---

## Mathematical Formulation

The Markowitz Mean-Variance Optimization objective is given by:

$$\min_{\mathbf{x}} \left[ q \mathbf{x}^T \boldsymbol{\Sigma} \mathbf{x} - (1-q) \boldsymbol{\mu}^T \mathbf{x} \right]$$

$$\text{subject to } \sum_{i=1}^{n} x_i = B, \quad x_i \in \{0, 1\}$$

Where:
- $\mathbf{x} \in \{0, 1\}^n$ is the binary asset selection vector.
- $\boldsymbol{\Sigma}$ is the $n \times n$ annualized asset covariance matrix.
- $\boldsymbol{\mu}$ is the annualized expected return vector.
- $q \in [0, 1]$ is the user-defined risk-aversion parameter.
- $B$ is the target portfolio budget size (number of assets to select).

To make this suitable for quantum processing, the budget constraint is penalized and mapped into an unconstrained **QUBO** cost function:

$$H(\mathbf{x}) = q \sum_{i,j} \Sigma_{i,j} x_i x_j - (1-q) \sum_{i} \mu_i x_i + P \left( \sum_{i} x_i - B \right)^2$$

where $P \gg 0$ is the penalty factor enforcing constraint satisfaction.

---

## Project Structure

quantum-portfolio-optimizer/├── data/│   └── fetcher.py         # Financial data retrieval and returns preprocessing├── quantum/│   ├── qubo.py            # Converts MPT matrices into Qiskit QuadraticProgram QUBOs│   └── solver.py          # QAOA variational algorithm implementation (Qiskit 2.x)├── utils/│   └── visualization.py   # Portfolio allocation and quantum state probability plotting├── main.py                # Command-Line Interface (CLI) application entry point├── app.py                 # Interactive Streamlit Web UI dashboard├── requirements.txt       # Production dependencies├── .gitignore             # Version control exclusions└── README.md              # Project documentation
---

## Installation & Setup

### Prerequisites

- **Python:** `3.10` to `3.13`
- **Git**

### 1. Clone the Repository

```bash
git clone [https://github.com/your-username/quantum-portfolio-optimizer.git](https://github.com/your-username/quantum-portfolio-optimizer.git)
cd quantum-portfolio-optimizer
2. Create and Activate Virtual EnvironmentOn Windows (PowerShell):PowerShellpython -m venv venv
.\venv\Scripts\Activate.ps1
On macOS / Linux:Bashpython3 -m venv venv
source venv/bin/activate
3. Install DependenciesBashpip install --upgrade pip
pip install -r requirements.txt
Usage GuideCommand-Line Execution (CLI)Run main.py to test the full quantum compilation and solution pipeline directly from the terminal:Bashpython main.py
Interactive Streamlit Web ApplicationLaunch the web application to adjust tickers, change risk parameters, and inspect allocation outputs interactively:Bashstreamlit run app.py
Upon launch, navigate to http://localhost:8501 in your browser.Core TechnologiesModuleTechnologyQuantum SDKQiskit 2.x, Qiskit Optimization, Qiskit Algorithms, Qiskit AerFinancial Engineyfinance, Pandas, NumPyData VisualizationMatplotlib, SeabornDashboard InterfaceStreamlitLicenseDistributed under the MIT License. See LICENSE for details.
<ElicitationsGroup message="Would you like any additional repository files?">
  <Elicitation label="Generate requirements.txt file content" query="Provide the exact raw copy-paste content for the requirements.txt file."/>
  <Elicitation label="Generate MIT License file content" query="Provide the raw copy-paste content for an MIT LICENSE file."/>
</ElicitationsGroup>
