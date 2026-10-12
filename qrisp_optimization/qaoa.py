import numpy as np
from qrisp import QuantumArray, QuantumVariable

from qrisp_optimization.qaoa_requirements import QAOARequirements


class QAOA[T]:
    def __init__(self, problem: QAOARequirements[T], qarg: QuantumVariable | QuantumArray) -> None:
        self.problem: QAOARequirements[T] = problem
        self.qarg: QuantumVariable | QuantumArray = qarg

    def ansatz(
        self,
        theta: np.ndarray
    ) -> QuantumVariable | QuantumArray:

        p = len(theta) // 2
        gammas, betas = theta[p:], theta[:p]

        self.problem.state_prep(self.qarg)
        for gamma, beta in zip(gammas, betas, strict=False):
            self.problem.cost_layer(self.qarg, gamma)
            self.problem.mixer_layer(self.qarg, beta)

        return self.qarg
