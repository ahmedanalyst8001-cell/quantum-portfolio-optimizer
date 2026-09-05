from qiskit_optimization import QuadraticProgram
from qiskit_optimization.converters import QuadraticProgramToQubo

def build_portfolio_qubo(mu, sigma, risk_factor: float = 0.5, budget: int = 2):
    num_assets = len(mu)
    qp = QuadraticProgram(name="PortfolioOptimization")

    for i in range(num_assets):
        qp.binary_var(name=f"x_{i}")

    linear = -1 * (1 - risk_factor) * mu
    quadratic = risk_factor * sigma

    qp.minimize(linear=linear, quadratic=quadratic)

    linear_constraint = {f"x_{i}": 1 for i in range(num_assets)}
    qp.linear_constraint(linear=linear_constraint, sense="==", rhs=budget, name="budget_constraint")

    converter = QuadraticProgramToQubo()
    qubo = converter.convert(qp)
    return qubo, qp