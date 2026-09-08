import numpy as np
from qrisp import QuantumArray, QuantumVariable
from qrisp_optimization.QAOA_Requirements import QAOA_Requirements

class LR_QAOA:
    def __init__(self, problem: QAOA_Requirements, qarg: QuantumVariable | QuantumArray):
        self.problem: QAOA_Requirements = problem
        self.qarg: QuantumVariable | QuantumArray = qarg

    def linear_ramp(start, stop, steps) -> np.ndarray:
        pass

    def ansatz(
        self, 
        depth: int,
        d_gamma: float,
        d_beta: float,
    ) -> QuantumVariable | QuantumArray:

        gammas = linear_ramp(0.0, d_gamma, depth)
        betas = linear_ramp(d_beta, 0.0, depth)

        self.problem.state_prep(self.qarg)
        for gamma, beta in zip(gammas, betas):
            self.problem.cost_layer(self.qarg, gamma)
            self.problem.mixer_layer(self.qarg, beta)

        return self.qarg