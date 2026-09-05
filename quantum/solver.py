from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit.primitives import StatevectorSampler

def solve_quantum_portfolio(qubo):
    # Sanitize QUBO matrix to ensure real coefficients only
    for key in list(qubo.objective.quadratic.coefficients.keys()):
        val = qubo.objective.quadratic.coefficients[key]
        if isinstance(val, complex):
            qubo.objective.quadratic.coefficients[key] = float(val.real)

    # Instantiate Qiskit 2.x Primitive Sampler
    sampler = StatevectorSampler()

    # Define optimizer and QAOA solver
    optimizer = COBYLA(maxiter=100)
    qaoa = QAOA(sampler=sampler, optimizer=optimizer, reps=2)

    quantum_optimizer = MinimumEigenOptimizer(qaoa)
    result = quantum_optimizer.solve(qubo)

    return result