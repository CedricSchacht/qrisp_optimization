import numpy as np
from qrisp import QuantumArray, QuantumVariable
from qrisp_optimization.QAOA_Requirements import QAOA_Requirements

class QAOA:
    def __init__(self, problem: QAOA_Requirements, qarg: QuantumVariable | QuantumArray):
        self.problem: QAOA_Requirements = problem
        self.qarg: QuantumVariable | QuantumArray = qarg

    def ansatz(
        self, 
        theta: np.ndarray
    ) -> QuantumVariable | QuantumArray:

        p = len(theta) // 2
        gammas, betas = theta[p:], theta[:p]

        self.problem.state_prep(self.qarg)
        for gamma, beta in zip(gammas, betas):
            self.problem.cost_layer(self.qarg, gamma)
            self.problem.mixer_layer(self.qarg, beta)

        return self.qarg